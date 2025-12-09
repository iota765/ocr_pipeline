from typing import Dict, Any, Optional
from io import BytesIO
import requests
from PIL import Image, ImageOps
from config import PEN_TO_PRINT_API_KEY, PEN_TO_PRINT_ENDPOINT
class PenToPrintClient:
    """
    Wrapper for Pen-to-Print Handwriting OCR on RapidAPI.
    Automatically fixes image rotation using EXIF before upload.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: str = PEN_TO_PRINT_ENDPOINT,
        session_value: str = "python-client",
    ):
        self.api_key = api_key or PEN_TO_PRINT_API_KEY
        self.endpoint = endpoint
        self.session_value = session_value

        if not self.api_key:
            raise ValueError("Pen-to-Print API key is required")

    def recognize_file(self, file_path: str) -> Dict[str, Any]:
        """
        Send an image file to the API and return the JSON response.
        Raises RuntimeError with a helpful message on API error.
        """

        # Open image and auto-fix orientation
        img = Image.open(file_path)
        img = ImageOps.exif_transpose(img)

        # Save to memory buffer as JPEG
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)

        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "pen-to-print-handwriting-ocr.p.rapidapi.com",
        }

        data = {
            "Session": self.session_value,
        }

        files = {
            "srcImg": ("image.jpg", buffer, "image/jpeg"),
        }

        resp = requests.post(
            self.endpoint,
            headers=headers,
            data=data,
            files=files,
            timeout=120,
        )

        # HTTP-level errors
        resp.raise_for_status()

        data = resp.json()

        # Pen-to-Print usually returns {"value": "..."} for recognized text
        if "value" not in data:
            raise RuntimeError(f"Unexpected response from Pen-to-Print API: {data}")

        return data

    @staticmethod
    def extract_text(data: Dict[str, Any]) -> str:
        """
        Extract the recognized text from API JSON.
        """
        val = data.get("value")
        if val is None:
            return ""
        if isinstance(val, list):
            return "\n".join(str(x) for x in val)
        return str(val)
