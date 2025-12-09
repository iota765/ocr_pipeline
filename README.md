# 🏥 Medical Handwriting OCR & PII Extraction Pipeline

A **batch OCR + PII extraction system** designed for handwritten **hospital case sheets, progress notes, and drug charts.**

---

## 🔍 What the pipeline does

It automatically:

- Reads **scanned handwritten medical documents** (`.jpg`, `.png`, `.pdf` → image per page)
- Calls an **OCR engine** (currently Pen-to-Print via RapidAPI)
- Normalizes raw text (removes noise, fixes spacing / line breaks)
- Extracts **structured PII & clinical data**, including:
  - Patient name, IPD No, UHID, Age, Sex, Bed No
  - Vitals (BP, PR, RR, Temperature)
  - Medications (drug name, dose, route, frequency)
  - Generic PII (dates, phone numbers, emails, etc.)
- Saves results to disk:
  - Raw OCR → `output/ocr_text/<image_name>.txt`
  - PII JSON → `output/pii_json/<image_name>.json`

🔧 The pipeline is tuned for **noisy handwriting + OCR mistakes commonly seen in hospitals.**

---

## 🧱 Tech Stack

| Purpose | Library |
|--------|---------|
| OCR API call | `requests` |
| Image handling & EXIF auto-rotation | `pillow` |
| Env vars & secrets | `python-dotenv` |
| Regex for PII & medical patterns | `regex` |
| Optional image preprocessing | `opencv-python`, `numpy` |

From `pyproject.toml`:

```toml
dependencies = [
    "numpy>=2.3.5",
    "opencv-python>=4.11.0.86",
    "pillow>=12.0.0",
    "python-dotenv>=1.2.1",
    "regex==2024.9.11",
    "requests>=2.32.5",
]
```

---

## 📁 Project Structure

```
ocr/
├─ pipeline.py              # Main entry point: batch process input/ → output/
├─ pen_to_print_client.py   # OCR wrapper (rotation fix + error handling)
├─ pii_extractor.py         # All regex logic: PII + vitals + medications
├─ config.py                # Loads API keys / endpoints from .env
├─ .env                     # Environment variables (NOT committed)
│
├─ input/                   # Place scanned images here (img1.jpg, img2.png, ...)
│
└─ output/
   ├─ ocr_text/             # Raw OCR text (img1.txt, img2.txt, ...)
   └─ pii_json/             # Extracted PII JSON (img1.json, img2.json, ...)
```

---

## ⚙️ Setup

### 1️⃣ Install Python & dependencies

Requirements:

- Python **3.10+**
- **uv** package manager

Install dependencies:

```bash
uv sync
```

(or without uv → manually add all dependencies listed above)

---

### 2️⃣ Environment variables

Create a `.env` file in the project root:

```
RAPIDAPI_KEY=your_rapidapi_key_here
```

---

## 🚀 Usage

Put your scanned images inside the `input/` folder.

Example:

```
input/
├─ img1.jpg
├─ img2.jpg
└─ img3.png
```

Run the pipeline:

```bash
uv run pipeline.py
```

📌 The script automatically detects all files inside `input/`.

---

### Example console output

```
📂 Found 3 file(s) in input/:
   → img1.jpg
   → img2.jpg
   → img3.png

🚀 Processing: img1.jpg
📝 OCR saved → output/ocr_text/img1.txt
🔐 PII saved → output/pii_json/img1.json
✔ Completed
```

---