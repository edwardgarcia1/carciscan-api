import re
from typing import Optional

import numpy as np
from paddleocr import PaddleOCR

# --- Global Model Cache ---
_ocr_model = None


def get_ocr_model():
    """
    Lazily initializes and returns a cached PaddleOCR instance
    with tuned parameters for document OCR.
    """
    global _ocr_model
    if _ocr_model is None:
        print("Loading PaddleOCR model...")
        _ocr_model = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            text_det_limit_side_len=480,
            text_det_limit_type="max",
            lang="en"
        )
        print("PaddleOCR model loaded")
    return _ocr_model


def extract_text_from_image(image_bytes: bytes) -> Optional[str]:
    """
    Extracts text from an image using PaddleOCR.

    Converts bytes → numpy array → OCR → extracts and joins `rec_texts`.

    Args:
        image_bytes: Raw bytes of the image.

    Returns:
        Normalized string of all detected text, or None on failure.
    """
    model = get_ocr_model()

    try:
        # Convert bytes to numpy array (OpenCV-style)
        import cv2

        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            print("Failed to decode image bytes")
            return None

        # Run OCR
        result = model.predict(img)

        # Collect all recognized text lines
        all_texts = []
        for res in result:
            texts = res["rec_texts"]
            if texts:
                all_texts.append(" ".join(texts))

        combined = " ".join(all_texts)
        return _normalize_ocr_text(combined)

    except Exception as e:
        print(f"An error occurred during OCR processing: {e}")
        return None


def _normalize_ocr_text(text: str) -> str:
    """
    Normalizes text: lowercase, collapse whitespace.
    """
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text.replace("\n", " ")).strip()
    return text


if __name__ == "__main__":
    # Quick local test — read an image directly into bytes
    try:
        with open("../../test_image.jpg", "rb") as f:
            image_bytes = f.read()

        print("--- Testing OCR Service (PaddleOCR) ---")
        extracted = extract_text_from_image(image_bytes)

        if extracted:
            print("✅ OCR successful!")
            print(extracted)
        else:
            print("❌ No text extracted.")

    except FileNotFoundError:
        print("❌ 'test_image.jpg' not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")
