from pathlib import Path

# Base directory is the project root where main.py lives
BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
TEXT_OUTPUT_DIR = OUTPUT_DIR / "text"
REDACTED_TEXT_OUTPUT_DIR = OUTPUT_DIR / "redacted_text"
REDACTED_IMAGE_OUTPUT_DIR = OUTPUT_DIR / "redacted_images"
LOG_DIR = OUTPUT_DIR / "logs"
TEMP_DIR = DATA_DIR / "temp"

# Ensure directories exist
for d in [
    INPUT_DIR,
    TEXT_OUTPUT_DIR,
    REDACTED_TEXT_OUTPUT_DIR,
    REDACTED_IMAGE_OUTPUT_DIR,
    LOG_DIR,
    TEMP_DIR,
]:
    d.mkdir(parents=True, exist_ok=True)
