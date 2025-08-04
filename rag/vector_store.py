import os
import chromadb
from typing import List, Dict, Any, Optional
from config import RAG_VECTOR_STORE

class VectorStore:
    """
    Class for managing vector storage and retrieval.
    """
    
    def __init__(self, collection_name: str = "ats_resume"):
        self.collection_name = collection_name
        self.client = None
        self.collection = None
        
        if RAG_VECTOR_STORE == "chroma":
            self._setup_chroma()
        # Add FAISS setup here if needed
    
    def _setup_chroma(self):
        """Setup ChromaDB vector store."""
        # Create persistent client
        persist_directory = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
        os.makedirs(persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
        except Exception:
            # If collection doesn't exist, create it
            self.collection = self.client.create_collection(name=self.collection_name)
    
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]] = None, ids: List[str] = None):
        """
        Add documents to the vector store.
        
        Args:
            documents (List[str]): List of document texts
            metadatas (List[Dict[str, Any]], optional): List of metadata dictionaries
            ids (List[str], optional): List of document IDs
        """
        if RAG_VECTOR_STORE == "chroma":
            self._add_chroma_documents(documents, metadatas, ids)
        # Add FAISS implementation here if needed
    
    def _add_chroma_documents(self, documents: List[str], metadatas: List[Dict[str, Any]] = None, ids: List[str] = None):
        """Add documents to ChromaDB."""
        # Generate embeddings
        from rag.embeddings import EmbeddingGenerator
        embedding_generator = EmbeddingGenerator()
        embeddings = embedding_generator.generate_embeddings(documents)
        
        # Add to collection
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
    
    def query(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query the vector store for similar documents.
        
        Args:
            query_text (str): Query text
            n_results (int): Number of results to return
            
        Returns:
            List[Dict[str, Any]]: List of similar documents with metadata
        """
        if RAG_VECTOR_STORE == "chroma":
            return self._query_chroma(query_text, n_results)
        # Add FAISS implementation here if needed
    
    def _query_chroma(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Query ChromaDB for similar documents."""
        # Generate query embedding
        from rag.embeddings import EmbeddingGenerator
        embedding_generator = EmbeddingGenerator()
        query_embedding = embedding_generator.generate_embedding(query_text)
        
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            result = {
                "document": results['documents'][0][i],
                "metadata": results['metadatas'][0][i] if results['metadatas'] else {},
                "id": results['ids'][0][i],
                "distance": results['distances'][0][i] if 'distances' in results else None
            }
            formatted_results.append(result)
        
        return formatted_results
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """
        Get all documents from the vector store.
        
        Returns:
            List[Dict[str, Any]]: List of all documents with metadata
        """
        if RAG_VECTOR_STORE == "chroma":
            return self._get_all_chroma_documents()
        # Add FAISS implementation here if needed
    
    def _get_all_chroma_documents(self) -> List[Dict[str, Any]]:
        """Get all documents from ChromaDB."""
        results = self.collection.get()
        
        formatted_results = []
        for i in range(len(results['documents'])):
            result = {
                "document": results['documents'][i],
                "metadata": results['metadatas'][i] if results['metadatas'] else {},
                "id": results['ids'][i]
            }
            formatted_results.append(result)
        
        return formatted_results
    
    def delete_document(self, doc_id: str):
        """
        Delete a document from the vector store.
        
        Args:
            doc_id (str): ID of the document to delete
        """
        if RAG_VECTOR_STORE == "chroma":
            self.collection.delete(ids=[doc_id])
        # Add FAISS implementation here if needed
    
    def update_document(self, doc_id: str, new_document: str, new_metadata: Dict[str, Any] = None):
        """
        Update a document in the vector store.
        
        Args:
            doc_id (str): ID of the document to update
            new_document (str): New document text
            new_metadata (Dict[str, Any], optional): New metadata
        """
        if RAG_VECTOR_STORE == "chroma":
            # Generate new embedding
            from rag.embeddings import EmbeddingGenerator
            embedding_generator = EmbeddingGenerator()
            new_embedding = embedding_generator.generate_embedding(new_document)
            
            # Update in collection
            self.collection.update(
                ids=[doc_id],
                documents=[new_document],
                embeddings=[new_embedding],
                metadatas=[new_metadata] if new_metadata else None
            )
        # Add FAISS implementation here if needed