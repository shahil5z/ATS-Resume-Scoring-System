import os
import sys
import subprocess
from data_initialization import initialize_rag_data

def initialize_system():
    """Initialize the ATS Resume Scoring System."""
    print("Initializing ATS Resume Scoring System...")
    
    # Create necessary directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/chroma_db", exist_ok=True)
    
    # Initialize RAG data
    print("Initializing RAG data...")
    try:
        initialize_rag_data()
        print("RAG data initialized successfully!")
    except Exception as e:
        print(f"Error initializing RAG data: {e}")
        print("Continuing without RAG data...")
    
    print("System initialization complete!")

def run_app():
    """Run the Streamlit app."""
    print("Starting Streamlit app...")
    subprocess.run(["streamlit", "run", "main.py"])

if __name__ == "__main__":
    initialize_system()
    run_app()