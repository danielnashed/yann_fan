from langchain.tools import BaseTool
from PIL import Image
import io
import pytesseract  # For OCR
from app.agent.tools.upload_image_to_s3_tool import ImageUploaderTool
# from .upload_image_to_s3_tool import ImageUploaderTool


class ImageParserTool(BaseTool):
    name: str = "image_parser"
    description: str = "Extracts text content from image file plus generates a public AWS S3 object url. Input should be bytes for content and string for filename. Output is a dictionary with image_url and extracted_text."
    
    def _run(self, content: bytes, filename: str) -> dict:
        try:
            # Open image from bytes
            bytes_object = io.BytesIO(content)
            image = Image.open(bytes_object)
            
            # Extract text using OCR if possible
            try:
                text = pytesseract.image_to_string(image)
            except:
                text = None
            
            # Upload image to S3 and get URL
            try:
                url = ImageUploaderTool()._run(content=content, filename=filename)
            except:
                url = None
            
            return {
                "url": url,
                "text": text
            }
            
        except Exception as e:
            return f"Error processing image or uploading to s3 bucket: {str(e)}"