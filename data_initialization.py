import os
from rag.retrieval import RAGRetriever

def initialize_rag_data():
    """Initialize the RAG system with industry benchmarks and best practices."""
    
    # Create RAG retriever
    try:
        retriever = RAGRetriever()
    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        return
    
    # Define industry benchmarks
    industry_benchmarks = [
        {
            "text": """
            Technology Industry Resume Benchmarks:
            - Average ATS score: 75/100
            - Top performer score: 90/100
            - Key skills weighted heavily: Programming languages, frameworks, tools
            - Experience requirements: Typically 3-5 years for mid-level positions
            - Education: Bachelor's degree often required, relevant certifications valued
            """,
            "metadata": {"type": "benchmark", "industry": "technology"}
        },
        {
            "text": """
            Healthcare Industry Resume Benchmarks:
            - Average ATS score: 70/100
            - Top performer score: 85/100
            - Key skills weighted heavily: Medical knowledge, certifications, patient care
            - Experience requirements: Varies by role, often 2+ years for clinical positions
            - Education: Specific degrees and licenses often required
            """,
            "metadata": {"type": "benchmark", "industry": "healthcare"}
        },
        {
            "text": """
            Finance Industry Resume Benchmarks:
            - Average ATS score: 72/100
            - Top performer score: 88/100
            - Key skills weighted heavily: Financial analysis, accounting, regulations
            - Experience requirements: Typically 3-5 years for analytical roles
            - Education: Finance, economics, or business degrees often required
            """,
            "metadata": {"type": "benchmark", "industry": "finance"}
        }
    ]
    
    # Define resume best practices
    best_practices = [
        {
            "text": """
            ATS-Friendly Resume Format Best Practices:
            - Use a clean, simple layout with standard section headers
            - Avoid graphics, images, and special characters
            - Use standard fonts like Arial, Calibri, or Times New Roman
            - Keep formatting consistent throughout the document
            - Use bullet points to describe experience and achievements
            - Save and submit as a PDF unless otherwise specified
            """,
            "metadata": {"type": "best_practice", "category": "format"}
        },
        {
            "text": """
            Resume Content Best Practices:
            - Tailor your resume to each job application
            - Include keywords from the job description
            - Quantify achievements with numbers and percentages
            - Use action verbs to begin bullet points
            - Focus on accomplishments rather than just responsibilities
            - Keep your resume concise (1-2 pages maximum)
            """,
            "metadata": {"type": "best_practice", "category": "content"}
        },
        {
            "text": """
            Technical Skills Section Best Practices:
            - Create a dedicated skills section
            - Include both technical and soft skills
            - Organize skills into categories (e.g., Programming Languages, Tools, Soft Skills)
            - List skills in order of proficiency or relevance to the job
            - Include specific technologies and methodologies
            - Avoid generic terms without context
            """,
            "metadata": {"type": "best_practice", "category": "skills"}
        },
        {
            "text": """
            Work Experience Section Best Practices:
            - List positions in reverse chronological order
            - Include company name, position title, dates, and location
            - Use 3-5 bullet points per position
            - Start bullet points with strong action verbs
            - Quantify achievements when possible (e.g., "Increased sales by 25%")
            - Focus on accomplishments relevant to the target job
            """,
            "metadata": {"type": "best_practice", "category": "experience"}
        }
    ]
    
    # Add documents to vector store
    try:
        documents = [doc["text"] for doc in industry_benchmarks + best_practices]
        metadatas = [doc["metadata"] for doc in industry_benchmarks + best_practices]
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        retriever.add_knowledge(documents, metadatas, ids)
        print("RAG data initialized successfully!")
    except Exception as e:
        print(f"Error adding documents to vector store: {e}")

if __name__ == "__main__":
    initialize_rag_data()