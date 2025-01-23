from langchain.tools import BaseTool
import os
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from typing import Optional, Type, List, Dict, Any
import requests
from pinecone import Pinecone

load_dotenv()
# load_dotenv(Path(__file__).parent.parent / '.env')

class VectorDBTool(BaseTool):
    """Tool for quering a vector database to retrieve relevant documents to answer a user question."""

    name: str = "vector_db"
    description: str = "Query pinecone vector database to retrieve relevant information."
    user_id: int = Field(..., description="The ID of the current user. It is an integer.")

    def __init__(self, user_id: int):
        super().__init__(user_id=user_id)

    def _run(self, query: str) -> Dict[str, Any]:
        """Execute vector search query."""
        try:
            print('agent using vector db tool now.')
            print('user id: ', str(self.user_id))
            print('query: ', query)
            index = connect_to_index()
            embeddings = get_embeddings(inputs=[query],  # List of text or image URLs
                                        dim=1024,
                                        JINA_API_KEY=os.getenv('JINA_API_KEY'),
                                        JINA_EMBEDDINGS_URL=os.getenv('JINA_EMBEDDINGS_URL'),
                                        task='retrieval.query'  # Set to 'retrieval.query' for text retrieval
            )
            query_embedding = embeddings["data"][0]["embedding"]

            results = index.query(
                namespace=str(self.user_id),
                vector=query_embedding,
                top_k=3,
                include_values=False,
                include_metadata=True
            )
            processed_results = '.\n'.join([f"{match['metadata']['content']}" for match in results['matches']])
            print('retrieval results from vector db: ', processed_results)
            return processed_results
        except Exception as e:
            return f"Query on vector database failed: {str(e)}"


# def embed_and_upsert(inputs: List[Dict[str, Any]], user_id: int) -> Dict[str, str]:
#     """Embed and upsert documents to vector database."""
#     try:
#         index = connect_to_index()
#         print('connected to index')
#         vectors = []
#         # Embed all documents and store them in vectors
#         for item in inputs:
#             embeddings = get_embeddings([item["content"]],
#                             dim=1024,
#                             JINA_API_KEY=os.getenv('JINA_API_KEY'),
#                             JINA_EMBEDDINGS_URL=os.getenv('JINA_EMBEDDINGS_URL'),
#                             ) 
#             print('embeddings created')
#             embedding = embeddings["data"][0]["embedding"]
#             vectors.append({
#                 "id": item['id'],
#                 "values": embedding,
#                 "metadata": {'content': item['content'], 'modality': item['modality']}
#             })
#         # Upsert all vectors to Pinecone
#         index.upsert(vectors=vectors, namespace=str(user_id))
#         print('upserted to vector database')
#         return {'message': 'Updated vector database successfully'}
#     except Exception as e:
#         raise RuntimeError(f"Upsert into vector database failed: {str(e)}")

def embed_and_upsert(inputs: List[Dict[str, Any]], user_id: int) -> Dict[str, str]:
    """Embed and upsert documents to vector database."""
    try:
        index = connect_to_index()
        print('connected to index')
        vectors = []
        formatted_inputs = [{i["modality"]: i["content"] } for i in inputs]
        # Embed all documents
        print('JINA_API_KEY: ', os.getenv('JINA_API_KEY'))
        print('JINA_EMBEDDINGS_URL: ', os.getenv('JINA_EMBEDDINGS_URL'))
        embeddings = get_embeddings(
                        inputs=formatted_inputs,
                        dim=1024,
                        JINA_API_KEY=os.getenv('JINA_API_KEY'),
                        JINA_EMBEDDINGS_URL=os.getenv('JINA_EMBEDDINGS_URL'),
                        ) 
        print('embeddings created')
        for i, embedding in enumerate(embeddings["data"]):
            vectors.append({
                "id": inputs[i]["id"],
                "values": embedding["embedding"],
                "metadata": {'content': inputs[i]["content"], 'modality': inputs[i]["modality"]}
            })
        print('vectors created')
        print('vectors: ', vectors)
        # Upsert all vectors to Pinecone
        index.upsert(vectors=vectors, namespace=str(user_id))
        print('upserted to vector database')
        return {'message': 'Updated vector database successfully'}
    except Exception as e:
        raise RuntimeError(f"Upsert into vector database failed: {str(e)}")

def get_embeddings(
    inputs: List[str],  # List of text or image URLs
    dim: int = 1024,
    JINA_API_KEY: str = None,
    JINA_EMBEDDINGS_URL: str = None,
    task: str = None  # Set to 'retrieval.query' for text retrieval
    ) -> Dict[str, Any]:
    try:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {JINA_API_KEY}'
        }
        data = {
            'input': inputs,
            'model': 'jina-clip-v2',
            'dimensions': dim,
            "normalized": True,
            "embedding_type": "float",
        }
        print("sending request to JINA Embedder")
        response = requests.post("https://api.jina.ai/v1/embeddings", headers=headers, json=data)
        print("received response from JINA Embedder", response)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request to JINA Embedder failed: {str(e)}")


def connect_to_index():
    PINECONE_INDEX_NAME = os.getenv('PINECONE_INDEX_NAME')
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    # Initialize Pinecone client and connect to index
    pc = Pinecone(api_key=PINECONE_API_KEY)
    print('initialized pinecone client')
    index = pc.Index(PINECONE_INDEX_NAME)
    print('created index')
    return index