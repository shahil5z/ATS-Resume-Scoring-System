from typing import List, Dict, Any, Optional
from openai import OpenAI
from config import OPENAI_API_KEY
from rag.vector_store import VectorStore

class RAGRetriever:
    """
    Class for retrieving and generating responses using RAG.
    """
    
    def __init__(self, collection_name: str = "ats_resume"):
        # Initialize vector store
        self.vector_store = VectorStore(collection_name)
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=OPENAI_API_KEY)
    
    def retrieve_relevant_documents(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query.
        
        Args:
            query (str): Query text
            n_results (int): Number of results to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of relevant documents
        """
        return self.vector_store.query(query, n_results)
    
    def generate_response(self, query: str, context: List[str]) -> str:
        """
        Generate a response using retrieved context.
        
        Args:
            query (str): User query
            context (List[str]): Retrieved context documents
            
        Returns:
            str: Generated response
        """
        # Combine context into a single string
        context_str = "\n\n".join(context)
        
        # Create prompt
        prompt = f"""
        You are an expert resume analyst and career coach. Based on the following context, provide a detailed and helpful response to the user's query.
        
        Context:
        {context_str}
        
        User Query:
        {query}
        
        Your Response:
        """
        
        # Generate response using OpenAI
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert resume analyst and career coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    def rag_query(self, query: str, n_results: int = 5) -> str:
        """
        Perform a complete RAG query.
        
        Args:
            query (str): User query
            n_results (int): Number of documents to retrieve
            
        Returns:
            str: Generated response
        """
        # Retrieve relevant documents
        documents = self.retrieve_relevant_documents(query, n_results)
        
        # Extract document texts
        context = [doc["document"] for doc in documents]
        
        # Generate response
        response = self.generate_response(query, context)
        
        return response
    
    def add_knowledge(self, documents: List[str], metadatas: List[Dict[str, Any]] = None, ids: List[str] = None):
        """
        Add knowledge documents to the vector store.
        
        Args:
            documents (List[str]): List of knowledge documents
            metadatas (List[Dict[str, Any]], optional): List of metadata dictionaries
            ids (List[str], optional): List of document IDs
        """
        self.vector_store.add_documents(documents, metadatas, ids)
    
    def get_industry_benchmarks(self, industry: str) -> Dict[str, Any]:
        """
        Get industry benchmarks using RAG.
        
        Args:
            industry (str): Industry name
            
        Returns:
            Dict[str, Any]: Industry benchmarks
        """
        query = f"What are the typical resume scoring benchmarks for the {industry} industry?"
        response = self.rag_query(query, n_results=3)
        
        # Parse response to extract benchmarks (this would need more sophisticated parsing in a real implementation)
        benchmarks = {
            "average": 70,
            "top": 85,
            "industry": industry
        }
        
        return benchmarks
    
    def get_resume_best_practices(self) -> List[str]:
        """
        Get resume best practices using RAG.
        
        Returns:
            List[str]: List of best practices
        """
        query = "What are the best practices for creating an ATS-friendly resume?"
        response = self.rag_query(query, n_results=5)
        
        # Parse response to extract best practices (this would need more sophisticated parsing in a real implementation)
        best_practices = [
            "Use a clean, professional format",
            "Include keywords from the job description",
            "Quantify your achievements with numbers",
            "Keep your resume to 1-2 pages",
            "Use standard section headers",
            "Avoid graphics and special characters",
            "Use bullet points for readability",
            "Tailor your resume to each job application"
        ]
        
        return best_practices