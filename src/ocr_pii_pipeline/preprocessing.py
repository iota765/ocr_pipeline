from pathlib import Path

import cv2
import numpy as np

from .config import TEMP_DIR


def preprocess_image(image_path: Path) -> Path:
    """
    Load image, grayscale, denoise, deskew.
    Save preprocessed image under data/temp and return its path.
    """
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")

    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Denoise while keeping edges (good for handwriting)
    gray = cv2.bilateralFilter(gray, 7, 75, 75)

    # Threshold for skew detection
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10,
    )

    # Deskew
    coords = np.column_stack(np.where(thresh < 255))
    if coords.size == 0:
        rotated = gray
    else:
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = gray.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            gray,
            M,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE,
        )

    out_path = TEMP_DIR / f"preprocessed_{image_path.name}"
    cv2.imwrite(str(out_path), rotated)
    return out_path
