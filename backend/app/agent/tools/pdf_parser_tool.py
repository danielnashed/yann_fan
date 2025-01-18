from langchain.tools import BaseTool
from pypdf import PdfReader
import io

class PDFParserTool(BaseTool):
    name: str = "pdf_parser"
    description: str = "Extracts text content from a PDF file. Input should be bytes object. Output is the extracted text content."

    def _run(self, content: bytes) -> str:
        try:
            pdf = PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            return f"Error processing PDF: {str(e)}"