import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

PEN_TO_PRINT_ENDPOINT = "https://pen-to-print-handwriting-ocr.p.rapidapi.com/recognize/"
PEN_TO_PRINT_API_KEY = os.getenv("RAPID_API_KEY")

if not PEN_TO_PRINT_API_KEY:
    raise RuntimeError(
        "❌ Pen-to-Print API key not found.\n"
        "Add to your .env, for example:\n\n"
        "RAPID_API_KEY=your_rapidapi_key_here\n"
    )