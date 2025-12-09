import re


def clean_text(text: str) -> str:
    """
    Basic cleanup of OCR text.
    """
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()
