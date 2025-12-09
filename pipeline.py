from pathlib import Path
import json
import traceback
from pen_to_print_client import PenToPrintClient
from pii_extractor import extract_pii


# ---------- directory auto-create ----------
BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
OCR_TEXT_DIR = OUTPUT_DIR / "ocr_text"
PII_JSON_DIR = OUTPUT_DIR / "pii_json"

for p in [OUTPUT_DIR, OCR_TEXT_DIR, PII_JSON_DIR]:
    p.mkdir(parents=True, exist_ok=True)


def process_file(file_path: Path, client: PenToPrintClient):
    print(f"\n🚀 Processing: {file_path.name}")

    base_name = file_path.stem  # img1.jpg → img1
    ocr_output_path = OCR_TEXT_DIR / f"{base_name}.txt"
    json_output_path = PII_JSON_DIR / f"{base_name}.json"

    # Skip if already processed
    if ocr_output_path.exists() and json_output_path.exists():
        print(f"⏭ Skipping {file_path.name} — already processed")
        return

    # ---------- OCR via Pen-to-Print ----------
    try:
        data = client.recognize_file(str(file_path))
        text = client.extract_text(data)
    except Exception as e:
        print(f"❌ Upload/OCR failed for {file_path.name}")
        print(e)
        return

    if not text.strip():
        print(f"⚠ No text returned for {file_path.name}")
        return

    # Save OCR text as imgX.txt
    ocr_output_path.write_text(text, encoding="utf-8")
    print(f"📝 OCR saved → {ocr_output_path}")

    # ---------- PII + meds extraction ----------
    try:
        pii = extract_pii(text)
        json_output_path.write_text(
            json.dumps(pii, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        print(f"🔐 PII saved → {json_output_path}")
    except Exception as e:
        print(f"❌ PII extraction failed for {file_path.name}")
        print(e)
        return

    print("✔ Completed")


if __name__ == "__main__":
    client = PenToPrintClient()

    files = list(INPUT_DIR.glob("*.*"))
    if not files:
        print("⚠ No files found in input/ folder.")
        raise SystemExit(0)

    print(f"📂 Found {len(files)} file(s) in input/:")
    for f in files:
        print("   →", f.name)

    for f in files:
        try:
            process_file(f, client)
        except Exception:
            print(f"\n❌ ERROR processing {f.name}")
            print(traceback.format_exc())
            continue
