from langchain.tools import BaseTool
from docx import Document
import io

class DOCXParserTool(BaseTool):
    name: str = "docx_parser"
    description: str = "Extracts text content from a docx file. Input should be bytes object. Output is the extracted text content."

    def _run(self, content: bytes) -> str:
        try:
            doc = Document(io.BytesIO(content))
            text = ""
            for page in doc.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return f"Error processing Docx: {str(e)}"