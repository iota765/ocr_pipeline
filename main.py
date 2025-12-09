from pathlib import Path
import json
import sys

# --------------------------
# Add src to import path
# --------------------------
BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"
sys.path.append(str(SRC_DIR))

from ocr_pii_pipeline.config import (
    INPUT_DIR,
    TEXT_OUTPUT_DIR,
    REDACTED_TEXT_OUTPUT_DIR,
    LOG_DIR,
)
from ocr_pii_pipeline.preprocessing import preprocess_image
from ocr_pii_pipeline.tesseract import run_ocr  # Tesseract inside
from ocr_pii_pipeline.cleaning import clean_text
from ocr_pii_pipeline.pii_detect import detect_pii
from ocr_pii_pipeline.redact_text import redact_text
from ocr_pii_pipeline.redact_image import redact_image


def process_single_image(image_path: Path):
    print(f"\n=== Processing: {image_path.name} ===")

    # 1. Preprocess
    preprocessed_path = preprocess_image(image_path)
    print(f"[1] Preprocessed image saved at: {preprocessed_path}")

    # 2. OCR
    raw_text, ocr_data = run_ocr(preprocessed_path)
    print("[2] OCR completed")

    # 3. Clean text
    clean = clean_text(raw_text)

    # 4. PII detection
    pii_list = detect_pii(clean)
    print(f"[3] PII items detected: {len(pii_list)}")

    # 5. Save clean text
    text_out = TEXT_OUTPUT_DIR / f"{image_path.stem}.txt"
    text_out.write_text(clean, encoding="utf-8")
    print(f"[4] Clean text saved to: {text_out}")

    # 6. Save PII log
    log_out = LOG_DIR / f"{image_path.stem}_pii.json"
    log_out.write_text(json.dumps(pii_list, indent=2), encoding="utf-8")
    print(f"[5] PII log saved to: {log_out}")

    # 7. Redacted text
    redacted_str = redact_text(clean, pii_list)
    redacted_out = REDACTED_TEXT_OUTPUT_DIR / f"{image_path.stem}_redacted.txt"
    redacted_out.write_text(redacted_str, encoding="utf-8")
    print(f"[6] Redacted text saved to: {redacted_out}")

    # 8. Redacted image
    redacted_img_path = redact_image(image_path, ocr_data, pii_list)
    print(f"[7] Redacted image saved to: {redacted_img_path}")

    print(f"=== Finished: {image_path.name} ===")


def main():
    images = (
        list(INPUT_DIR.glob("*.jpg"))
        + list(INPUT_DIR.glob("*.jpeg"))
        + list(INPUT_DIR.glob("*.png"))
    )

    if not images:
        print(f"No images found in input folder: {INPUT_DIR}")
        return

    print(f"Found {len(images)} image(s) in {INPUT_DIR}")
    for img in images:
        process_single_image(img)


if __name__ == "__main__":
    main()
