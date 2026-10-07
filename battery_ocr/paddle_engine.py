"""Lazy PaddleOCR adapter with a stable JSON-like result format."""

from typing import Any, List, Optional


class PaddleOCREngine:
    def __init__(self, language: str = "ch", use_gpu: bool = False):
        try:
            from paddleocr import PaddleOCR
        except ImportError as exc:  # pragma: no cover - depends on deployment extras
            raise RuntimeError("install paddleocr to enable the PaddleOCR engine") from exc
        try:
            self.ocr = PaddleOCR(
                lang=language,
                device="gpu" if use_gpu else "cpu",
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=False,
            )
        except TypeError:  # PaddleOCR 2.x compatibility
            self.ocr = PaddleOCR(lang=language, use_angle_cls=True, use_gpu=use_gpu)

    def recognize(self, image: Any) -> List[dict]:
        raw = self.ocr.predict(image) if hasattr(self.ocr, "predict") else self.ocr.ocr(image, cls=True)
        return _normalize_results(raw)


def _normalize_results(raw: Any) -> List[dict]:
    """Normalize PaddleOCR 2.x and 3.x outputs without assuming one version."""

    results: List[dict] = []

    def visit(node: Any) -> None:
        if isinstance(node, dict):
            text = node.get("rec_text") or node.get("text")
            score = node.get("rec_score", node.get("score", node.get("confidence")))
            if text is not None:
                try:
                    confidence = float(score) if score is not None else 0.0
                except (TypeError, ValueError):
                    confidence = 0.0
                if str(text).strip():
                    results.append({"text": str(text).strip(), "confidence": confidence, "engine": "paddleocr"})
            for value in node.values():
                visit(value)
            return
        if isinstance(node, (list, tuple)):
            if len(node) == 2 and isinstance(node[1], (list, tuple)) and len(node[1]) >= 1:
                text, score = node[1][0], node[1][1] if len(node[1]) > 1 else 0.0
                if isinstance(text, str) and text.strip():
                    results.append({"text": text.strip(), "confidence": float(score), "engine": "paddleocr"})
                    return
            for value in node:
                visit(value)

    visit(raw)
    return results
