"""Composable four-part battery nameplate OCR pipeline."""

from typing import Optional

from .localize import YoloEasyOCR
from .paddle_engine import PaddleOCREngine
from .preprocess import preprocess_image
from .qr_decoder import decode_codes, explicit_chemistry_from_text


class BatteryOCRPipeline:
    def __init__(self, yolo_model: Optional[str] = None, use_paddle: bool = True, paddle_language: str = "ch"):
        self.localizer = YoloEasyOCR(yolo_model) if yolo_model else None
        self.paddle = PaddleOCREngine(language=paddle_language) if use_paddle else None

    def run(self, image_path: str) -> dict:
        prepared = preprocess_image(image_path)
        codes = decode_codes(prepared.original)
        localized = self.localizer.recognize(prepared.original) if self.localizer else []
        paddle = self.paddle.recognize(prepared.binary) if self.paddle else []
        text_items = localized + paddle
        text = "\n".join(item["text"] for item in text_items if item.get("text"))
        explicit = [explicit_chemistry_from_text(item["text"]) for item in text_items]
        explicit += [explicit_chemistry_from_text(item["text"]) for item in codes]
        evidence = [item for item in explicit if item]
        chemistries = sorted({item["chemistry"] for item in evidence})
        return {
            "ocr_text": text,
            "regions": localized,
            "codes": codes,
            "ocr_engines": sorted({item.get("engine", "easyocr") for item in text_items}),
            "chemistry": chemistries[0] if len(chemistries) == 1 else "UNKNOWN",
            "chemistry_evidence": evidence,
            "chemistry_conflict": len(chemistries) > 1,
        }
