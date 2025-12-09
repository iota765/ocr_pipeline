# Medical Handwriting OCR & PII Extraction Pipeline

This project is a **batch OCR + PII extraction pipeline** for handwritten **hospital case sheets, progress notes, and drug charts**.

It:

- Reads **handwritten medical documents** (JPG/PNG/PDF → image).
- Uses an **OCR engine** (currently Pen-to-Print via RapidAPI).
- Normalizes the raw text.
- Extracts **structured PII + clinical info**, including:
  - Patient name, IPD No, UHID, Age, Sex, Bed No
  - Vitals (BP, PR, RR, Temperature)
  - Medications (drug name, dose, route, frequency)
  - Generic PII (dates, phones, emails, etc.)
- Saves:
  - OCR text as `output/ocr_text/<image_name>.txt`
  - PII JSON as `output/pii_json/<image_name>.json`

This pipeline was built specifically around **real hospital documents** and tuned for noisy handwriting + OCR errors.

---

## 🧱 Tech Stack

Core libraries used:

- `requests` – calling the OCR API (Pen-to-Print via RapidAPI)
- `pillow` – image loading and **auto-rotation** (EXIF-based)
- `python-dotenv` – managing secrets via `.env`
- `regex` – robust pattern matching for PII & meds

## Dependencies (from `pyproject.toml`):

```toml
dependencies = [
    "numpy>=2.3.5",
    "opencv-python>=4.11.0.86",
    "pillow>=12.0.0",
    "python-dotenv>=1.2.1",
    "regex==2024.9.11",
    "requests>=2.32.5",
]
📁 Project Structure
ocr/
├─ pipeline.py              # Main entry point: batch process input/ → output/
├─ pen_to_print_client.py   # RapidAPI Pen-to-Print OCR wrapper (with rotation fix)
├─ pii_extractor.py         # All regex logic: PII + clinical + medications
├─ config.py                # Loads API keys / endpoints from .env
├─ .env                     # Environment variables (NOT committed)
│
├─ input/                   # Put your scanned images here (img1.jpg, img2.jpg, ...)
│
└─ output/
   ├─ ocr_text/             # Raw OCR text files (img1.txt, img2.txt, ...)
   └─ pii_json/             # Extracted PII in JSON per image

⚙️ Setup
1. Python & uv

Make sure you have:

Python 3.10+

uv
installed

Then in your project folder:

uv sync


(or, if you’re not using uv yet: uv add the dependencies listed above)

2. Environment variables (.env)

Create a .env file in the project root:
RAPIDAPI_KEY=your_rapidapi_key_here

🚀 Usage

Drop your images into the input/ folder
Examples:

input/
├─ img1.jpg   # progress report
├─ img2.jpg   # drug administration chart
└─ img3.jpg   # another case sheet


Run the pipeline:

uv run pipeline.py


The script will:

Auto-detect all files in input/

Example output:

📂 Found 3 file(s) in input/:
   → img1.jpg
   → img2.jpg
   → img3.jpg

🚀 Processing: img1.jpg
📝 OCR saved → output/ocr_text/img1.txt
🔐 PII saved → output/pii_json/img1.json
✔ Completed

🚀 Processing: img2.jpg
...
