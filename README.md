# OCR + PII Extraction for Handwritten Medical Documents

This project performs **OCR and automatic PII redaction** on handwritten medical sheets (progress notes / admission forms).  
It extracts text from scanned pages, detects sensitive patient information (PII), and **removes it from both the text and the image** to ensure complete privacy protection.

---

## 🔄 Pipeline Overview
Input Image
→ Preprocessing (grayscale, denoise, deskew)
→ OCR (Tesseract)
→ Text Cleaning
→ PII Detection (Regex)
→ Redacted Text + Redacted Image

## Folder Structure
data/input/ → input handwritten images
data/output/text/ → extracted OCR text
data/output/redacted_text/ → PII-masked text
data/output/redacted_images/→ images with black boxes over PII
data/output/logs/ → PII JSON logs
data/temp/ → preprocessed images used for OCR

---

## ⚠ OCR Engine Notice (Tesseract vs Google Vision)

The pipeline was originally designed for **Google Cloud Vision OCR**, but the Vision API requires **billing / paid usage**.  
To make this project **fully free and runnable anywhere**, the OCR component was switched to **local Tesseract OCR**.

## The code is modular — switching back to Google Vision or AWS Textract would only require replacing the OCR function, without modifying the rest of the pipeline.

---

## ▶ How to Run

### 1️⃣ Install dependencies
pip install -r requirements.txt

### 2️⃣ Install Tesseract OCR (Windows)
Download: https://github.com/UB-Mannheim/tesseract/wiki

If needed, set executable path in code:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
3️⃣ Add input images

Place .jpg/.jpeg/.png files into:

data/input/

4️⃣ Run the pipeline
python main.py

