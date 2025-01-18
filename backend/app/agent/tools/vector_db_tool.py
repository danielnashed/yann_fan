from langchain.tools import BaseTool
import os
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Optional, Type, List, Dict, Any
import requests
from pinecone import Pinecone


load_dotenv(Path(__file__).parent.parent / '.env')

class VectorDBTool(BaseTool):
    """Tool for managing vector database operations using Pinecone and Jina."""

    name: str = "vector_db"
    description: str = "Query pinecone vector database. Supported documents includes PDF, docx, and images."
    user_id: int = Field(..., description="The ID of the current user.")

    def __init__(self, user_id: int):
        super().__init__(
            name=self.name, 
            description=self.description,
            user_id=user_id
        )
        self.JINA_EMBEDDINGS_URL = os.getenv('JINA_EMBEDDINGS_URL')
        self.PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
        self.JINA_API_KEY = os.getenv('JINA_API_KEY')
        self.DIM = 1024
        # Initialize Pinecone client and connect to index
        self.pc = Pinecone(api_key=self.JINA_API_KEY)
        self.index = self.pc.Index(self.PINECONE_INDEX_NAME)


    def _run(self, query: str) -> Dict[str, Any]:
        """Execute vector search query."""
        try:
            embeddings = self.get_embeddings([query], task='retrieval.query')
            query_embedding = embeddings["data"][0]["embedding"]

            results = self.index.query(
                vector=query_embedding,
                top_k=3,
                include_values=False,
                include_metadata=True
            )
            print(results)
            return results
        except Exception as e:
            return f"Query on vector database failed: {str(e)}"


    def embed_and_upsert(self, inputs: List[Dict[str, Any]]) -> Dict[str, str]:
        """Embed and upsert documents to vector database."""
        try:
            vectors = []
            # Embed all documents and store them in vectors
            for item in inputs:
                embeddings = self.get_embeddings([item["content"]])
                embedding = embeddings["data"][0]["embedding"]
                vectors.append({
                    "id": item['id'],
                    "values": embedding,
                    "metadata": {'content': item['content'], 'modality': item['modality']}
                })
            # Upsert all vectors to Pinecone
            self.index.upsert(vectors=vectors)
            return {'message': 'Updated vector database successfully'}
        except Exception as e:
            raise RuntimeError(f"Upsert into vector database failed: {str(e)}")
        

    def get_embeddings(
        self,
        inputs: List[str],  # List of text or image URLs
        task: str = None  # Set to 'retrieval.query' for text retrieval
        ) -> Dict[str, Any]:
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.JINA_API_KEY}'
            }
            data = {
                'input': inputs,
                'model': 'jina-clip-v2',
                'dimensions': self.DIM,
                "normalized": True,
                "embedding_type": "float",
            }

            response = requests.post(self.JINA_EMBEDDINGS_URL, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request to JINA Embedder failed: {str(e)}")
