import os
from typing import List
from openai import OpenAI
from config import OPENAI_API_KEY, RAG_EMBEDDING_MODEL

class EmbeddingGenerator:
    """
    Class for generating embeddings using OpenAI's API.
    """
    
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = RAG_EMBEDDING_MODEL
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate an embedding for the given text.
        
        Args:
            text (str): Text to embed
            
        Returns:
            List[float]: Embedding vector
        """
        response = self.client.embeddings.create(
            input=text,
            model=self.model
        )
        
        return response.data[0].embedding
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.
        
        Args:
            texts (List[str]): List of texts to embed
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        
        return [data.embedding for data in response.data]