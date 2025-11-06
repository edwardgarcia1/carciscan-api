import io
import tempfile
from typing import Optional

# Pillow for image handling
from PIL import Image

# DocTR imports
from doctr.io import DocumentFile
from doctr.models import ocr_predictor

# --- Global Model Cache ---
_ocr_model = None


def get_ocr_model():
    """Loads the OCR model if it hasn't been loaded yet."""
    global _ocr_model
    if _ocr_model is None:
        print("Loading DocTR OCR model... (this may take a moment on first run)")
        _ocr_model = ocr_predictor(pretrained=True)
        print("✅ DocTR OCR model loaded successfully.")
    return _ocr_model


def extract_text_from_image(image_bytes: bytes) -> Optional[str]:
    """
    Extracts text from an image using DocTR by writing bytes to a temporary file.

    Args:
        image_bytes: The raw bytes of the image file.

    Returns:
        A single string containing all extracted text, or None if extraction fails.
    """
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
        full_text = result.render()

        return full_text

    except Exception as e:
        print(f"An error occurred during OCR processing: {e}")
        return None
    finally:
        # 5. IMPORTANT: Clean up the temporary file
        import os
        if os.path.exists(temp_path):
            os.remove(temp_path)


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