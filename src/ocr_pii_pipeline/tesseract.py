from pathlib import Path
import cv2
import pytesseract
from pytesseract import Output

# Tell pytesseract exactly where tesseract.exe is installed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def run_ocr(image_path: Path):
    """
    Run local Tesseract OCR on the (preprocessed) image.
    Returns:
      - full text string
      - word-level OCR data dict (for image redaction)
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # PSM tuned for sparse/handwritten text
    custom_config = r"--oem 1 --psm 11"
    text = pytesseract.image_to_string(rgb, config=custom_config)

    data = pytesseract.image_to_data(rgb, output_type=Output.DICT)

    return text, data
