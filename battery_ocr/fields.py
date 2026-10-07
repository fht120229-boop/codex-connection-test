"""Conservative extraction of common nameplate fields from OCR text."""

import re
from typing import Dict

from .qr_decoder import explicit_chemistry_from_text


def extract_structured_fields(text: str) -> Dict[str, str]:
    """Extract fields only when the text contains an explicit label/value pair."""

    fields: Dict[str, str] = {}
    labelled = {
        "brand": r"(?:品牌|brand|manufacturer|厂商)\s*[:：]?\s*([^\n,，;；]+)",
        "model": r"(?:型号|model|part\s*no\.?|p/?n)\s*[:：]?\s*([^\n,，;；]+)",
        "production_date": r"(?:生产日期|制造日期|date)\s*[:：]?\s*([^\n,，;；]+)",
    }
    for name, pattern in labelled.items():
        match = re.search(pattern, text or "", flags=re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            if value:
                fields[name] = value
    for name, pattern in (
        ("voltage", r"\b(\d+(?:\.\d+)?)\s*V\b"),
        ("capacity", r"\b(\d+(?:\.\d+)?)\s*(?:Ah|安时)\b"),
        ("energy", r"\b(\d+(?:\.\d+)?)\s*Wh\b"),
    ):
        match = re.search(pattern, text or "", flags=re.IGNORECASE)
        if match:
            fields[name] = match.group(1)
    chemistry = explicit_chemistry_from_text(text or "")
    if chemistry:
        fields["chemistry"] = chemistry["chemistry"]
        fields["chemistry_evidence"] = chemistry["matched_text"]
    return fields
