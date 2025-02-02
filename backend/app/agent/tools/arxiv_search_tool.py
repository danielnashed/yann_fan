from langchain.tools import BaseTool
from langchain_community.retrievers import ArxivRetriever
from pypdf import PdfReader
from pydantic import BaseModel, Field
import io
from typing import List, Dict
import re
import uuid
from .utils import chunk_text_by_paragraphs
from app.agent.tools.vector_db_tool import embed_and_upsert, VectorDBTool

class ArXivSearchTool(BaseTool):
    name: str = "search_arxiv"
    description: str = "Search and retrieve scientific articles from 'Arxiv.org'. Input should be a query string. Output is the extracted text content."
    user_id: int = Field(..., description="The ID of the current user.")

    def __init__(self, user_id: int):
        super().__init__(user_id=user_id)

    def _run(self, query: str, max_chunk_size: int = 2000, min_chunk_size: int = 1500) -> List:
        try:
            # Retrieve a single paper from Arxiv and extract a summary text from paper. Input is a query string. Output is the extracted text content.
            retriever = ArxivRetriever(load_max_docs=1)
            doc = retriever.invoke(query + " Yann LeCun")
            text = doc.page_content
            metadata = doc.metadata

            # Remove invalid unicode characters
            cleaned_text = re.sub(r"/uni[0-9a-fA-F]+", "", text).strip()

            # Replace tabs with spaces to save space in context window
            cleaned_text = cleaned_text.replace("\t", " ")

            # Chunk the extracted text
            chunks = chunk_text_by_paragraphs(cleaned_text, max_chunk_size, min_chunk_size)[:5]

            # Add chunks to processed files list
            clean_filename = '_'.join(metadata["Title"].split())
            id = clean_filename +  '_' + str(uuid.uuid4())[:8]
            processed_files = []

            for i, chunk in enumerate(chunks):
                print(f'\n\nProcessing chunk {i+1}: {chunk}')
                processed_files.append({
                    "id": f"{id}_{i}",
                    "modality": 'text',
                    "content": chunk,
                })

            # Upsert to vector database
            response = embed_and_upsert(inputs=processed_files, user_id=self.user_id)
            print('upserted to vector database. Done now.')

            # Run vector database tool to retrieve relevant chunks 
            vector_db_tool = VectorDBTool(user_id=self.user_id)
            processed_results = vector_db_tool._run(query)

            return processed_results
        
        except Exception as e:
            return f"Error processing PDF: {str(e)}"