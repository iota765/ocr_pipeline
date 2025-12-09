import re
from typing import List, Dict

PII_PATTERNS = {
    "uhid": r"UHID\s*No[:\s]*\d+",
    "ipd": r"IPD\s*No[:\s]*\d+",
    "name_line": r"(Patient\s*Name|Name)[:\s]*[A-Za-z ]+",
    "age": r"Age[:\s]*\d+\s*[Yy]?",
    "date": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    "bed_no": r"Bed\s*No[:\s]*\d+",
    "phone": r"\+?\d[\d\-\s]{8,}\d",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
}


def detect_pii(text: str) -> List[Dict]:
    """
    Scan text with regex patterns and return list of PII spans.
    Each item: {type, value, start, end}
    """
    results: List[Dict] = []
    for pii_type, pattern in PII_PATTERNS.items():
        for m in re.finditer(pattern, text):
            results.append(
                {
                    "type": pii_type,
                    "value": m.group(),
                    "start": m.start(),
                    "end": m.end(),
                }
            )
    return results
