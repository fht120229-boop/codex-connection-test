"""Dedicated QR/barcode decoding and explicit chemistry evidence parsing."""

import re
from typing import Any, List, Optional

def decode_codes(image: Any) -> List[dict]:
    """Decode QR codes with OpenCV and optionally barcodes with zxing-cpp."""

    try:
        import cv2
    except ImportError as exc:  # pragma: no cover - deployment dependency
        raise RuntimeError("install opencv-python-headless to decode QR codes") from exc
    decoder = cv2.QRCodeDetector()
    results: List[dict] = []
    try:
        ok, values, _, _ = decoder.detectAndDecodeMulti(image)
        if ok:
            for value in values or []:
                if value:
                    results.append({"text": value, "format": "QR_CODE", "engine": "opencv"})
    except (cv2.error, ValueError):
        pass
    if not results:
        try:
            value, _, _ = decoder.detectAndDecode(image)
            if value:
                results.append({"text": value, "format": "QR_CODE", "engine": "opencv"})
        except cv2.error:
            pass
    try:  # Optional broad barcode coverage.
        import zxingcpp
        for item in zxingcpp.read_barcodes(image):
            text = getattr(item, "text", "")
            if text and not any(x["text"] == text for x in results):
                results.append({"text": text, "format": str(getattr(item, "format", "BARCODE")), "engine": "zxing-cpp"})
    except ImportError:
        pass
    return results


_CHEMISTRY_PATTERNS = (
    ("LFP", re.compile(r"(?:磷酸铁锂|磷酸铁锂电|\bLFP\b|\bLiFePO4\b)", re.I)),
    ("NMC", re.compile(r"(?:三元锂|三元锂电|\bNMC\b|\bNCM\b|\bTernary\b)", re.I)),
    ("NCA", re.compile(r"\bNCA\b", re.I)),
    ("LMO", re.compile(r"锰酸锂|\bLMO\b", re.I)),
    ("LCO", re.compile(r"钴酸锂|\bLCO\b", re.I)),
    ("LEAD_ACID", re.compile(r"铅酸|lead[- ]?acid", re.I)),
)


def explicit_chemistry_from_text(text: str) -> Optional[dict]:
    """Return chemistry only when an explicit marker is present in the text."""

    for chemistry, pattern in _CHEMISTRY_PATTERNS:
        match = pattern.search(text or "")
        if match:
            return {"chemistry": chemistry, "matched_text": match.group(0), "explicit": True}
    return None
