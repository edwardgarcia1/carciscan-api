import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""
os.environ["OPENCV_OPENCL_RUNTIME"] = "disabled"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import io
import tempfile
from typing import Optional
import re

# Pillow for image handling
from PIL import Image

# --- Global Model Cache ---
_ocr_model = None


def get_ocr_model():
    global _ocr_model
    if _ocr_model is None:
        print("Loading DocTR OCR model...")
        from doctr.models import ocr_predictor  # ← move here
        _ocr_model = ocr_predictor(pretrained=True)
        print("OCR model loaded")
    return _ocr_model


def extract_text_from_image(image_bytes: bytes) -> Optional[str]:
    """
    Extracts text from an image using DocTR by writing bytes to a temporary file.

    Args:
        image_bytes: The raw bytes of the image file.

    Returns:
        A single string containing all extracted text, or None if extraction fails.
    """

    from doctr.io import DocumentFile
    model = get_ocr_model()

    # Create a temporary file. `delete=False` allows us to close the file
    # before DocTR opens it. We will manually delete it in the `finally` block.
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    temp_path = temp_file.name

    try:
        # 1. Write the image bytes to the temporary file
        temp_file.write(image_bytes)
        temp_file.close()  # Close the file so DocTR can access it

        # 2. Pass the temporary file's path to DocTR, just like in your working example
        doc = DocumentFile.from_images(temp_path)

        # 3. Run the OCR
        result = model(doc)

        # 4. The result object is rich, but for our purpose, we just need the full text.
        full_text = _normalize_ocr_text(result.render())

        return full_text

    except Exception as e:
        print(f"An error occurred during OCR processing: {e}")
        return None
    finally:
        # 5. IMPORTANT: Clean up the temporary file
        import os
        if os.path.exists(temp_path):
            os.remove(temp_path)


def _normalize_ocr_text(text: str) -> str:
    """
    Normalizes OCR text to make it easier to parse.
    - Converts to lowercase.
    - Replaces newlines with a single space.
    - Collapses multiple spaces into one.
    """
    if not text:
        return ""

    # Convert to lowercase
    normalized_text = text.lower()

    # Replace newlines with a space
    normalized_text = normalized_text.replace('\n', ' ')

    # Collapse multiple spaces into a single space
    normalized_text = re.sub(r'\s+', ' ', normalized_text).strip()

    return normalized_text

# --- Test Block ---
if __name__ == '__main__':
    # To test this, you need an image file named 'test_image.png' in your project root.
    try:
        with open("../../test_image.jpg", "rb") as f:
            image_bytes = f.read()

        print("--- Testing OCR Service ---")
        extracted_text = extract_text_from_image(image_bytes)

        if extracted_text:
            print("✅ OCR successful!")
            print("Extracted Text:")
            print(extracted_text)
        else:
            print("❌ OCR failed or returned no text.")

    except FileNotFoundError:
        print("❌ Test failed: 'test_image.png' not found in the project root.")
        print("Please create a test image to run this test.")
    except Exception as e:
        print(f"An unexpected error occurred during the test: {e}")