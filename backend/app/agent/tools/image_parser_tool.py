from langchain.tools import BaseTool
from PIL import Image
import io
import pytesseract  # For OCR

class ImageParserTool(BaseTool):
    name: str = "image_parser"
    description: str = "Extracts text content and metadata from image files. Input should be bytes object."

    def _run(self, content: bytes) -> str:
        try:
            # Open image from bytes
            image = Image.open(io.BytesIO(content))
            
            # Get image metadata
            metadata = {
                "format": image.format,
                "size": image.size,
                "mode": image.mode
            }
            
            # Extract text using OCR if possible
            try:
                text = pytesseract.image_to_string(image)
            except:
                text = "No text extracted"
            
            return {
                "metadata": metadata,
                "extracted_text": text
            }
            
        except Exception as e:
            return f"Error processing image: {str(e)}"