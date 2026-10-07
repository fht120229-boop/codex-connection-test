"""YOLO text-region localization followed by EasyOCR recognition.

Both dependencies are optional. The adapter only loads them when a model is
configured, so the rest of the pipeline can still run with PaddleOCR alone.
"""

from dataclasses import asdict, dataclass
from typing import Any, List, Optional, Sequence

@dataclass
class TextRegion:
    box: List[int]
    text: str
    confidence: float
    detector: str = "yolo"
    recognizer: str = "easyocr"


class YoloEasyOCR:
    def __init__(self, model_path: Optional[str] = None, languages: Sequence[str] = ("ch_sim", "en")):
        if not model_path:
            raise ValueError("model_path is required for the YOLO→EasyOCR adapter")
        try:
            from ultralytics import YOLO
            import easyocr
        except ImportError as exc:  # pragma: no cover - depends on deployment extras
            raise RuntimeError("install ultralytics and easyocr to enable YOLO→EasyOCR") from exc
        self.detector = YOLO(model_path)
        self.reader = easyocr.Reader(list(languages), gpu=False)

    def _boxes(self, image: Any) -> List[List[int]]:
        result = self.detector.predict(source=image, conf=0.25, verbose=False)[0]
        boxes = getattr(getattr(result, "boxes", None), "xyxy", None)
        if boxes is None:
            return []
        return [[int(v) for v in row] for row in boxes.cpu().tolist()]

    def recognize(self, image: Any) -> List[dict]:
        regions = self._boxes(image)
        if not regions:
            regions = [[0, 0, image.shape[1], image.shape[0]]]
        output: List[dict] = []
        for x1, y1, x2, y2 in regions:
            x1, y1 = max(0, x1), max(0, y1)
            crop = image[y1:max(y1 + 1, y2), x1:max(x1 + 1, x2)]
            for item in self.reader.readtext(crop):
                if len(item) < 3:
                    continue
                text, confidence = str(item[1]).strip(), float(item[2])
                if text and confidence >= 0.25:
                    output.append(asdict(TextRegion([x1, y1, x2, y2], text, confidence)))
        return output
