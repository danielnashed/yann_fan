from langchain.tools import BaseTool
from pypdf import PdfReader
import io
from typing import List, Dict
import re
from .utils import chunk_text_by_paragraphs

class PDFParserTool(BaseTool):
    name: str = "pdf_parser"
    description: str = "Extracts text content from a PDF file. Input should be bytes object. Output is the extracted text content."

    def _run(self, content: bytes, max_chunk_size: int = 1500, min_chunk_size: int = 500) -> List:
        try:
            pdf = PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
                # page.images

            # Remove invalid unicode characters
            cleaned_text = re.sub(r"/uni[0-9a-fA-F]+", "", text).strip()

            # Replace tabs with spaces to save space in context window
            cleaned_text = cleaned_text.replace("\t", " ")
            
            # Chunk the extracted text
            chunks = chunk_text_by_paragraphs(cleaned_text, max_chunk_size, min_chunk_size)
            return chunks
        
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
        

