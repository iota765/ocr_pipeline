from typing import List, Dict
from pathlib import Path

import cv2

from .config import REDACTED_IMAGE_OUTPUT_DIR


def redact_image(
    original_image_path: Path,
    ocr_data: Dict,
    pii_list: List[Dict],
) -> Path:
    """
    Draw black rectangles over words whose text is part of any PII string.
    Uses Tesseract's image_to_data output (ocr_data).
    """
    img = cv2.imread(str(original_image_path))
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {original_image_path}")

    if not ocr_data or "text" not in ocr_data:
        out_path = REDACTED_IMAGE_OUTPUT_DIR / f"redacted_{original_image_path.name}"
        cv2.imwrite(str(out_path), img)
        return out_path

    pii_values = [p["value"] for p in pii_list]

    n_boxes = len(ocr_data["text"])
    for i in range(n_boxes):
        word = ocr_data["text"][i]
        if not word or not word.strip():
            continue

        if any(word in v for v in pii_values):
            x = ocr_data["left"][i]
            y = ocr_data["top"][i]
            w = ocr_data["width"][i]
            h = ocr_data["height"][i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)

    out_path = REDACTED_IMAGE_OUTPUT_DIR / f"redacted_{original_image_path.name}"
    cv2.imwrite(str(out_path), img)
    return out_path
