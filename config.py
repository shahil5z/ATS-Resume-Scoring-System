import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database Configuration
DB_TYPE = os.getenv("DB_TYPE", "sqlite")  # Options: "sqlite", "mongodb"

# Database paths and URIs (always define these to avoid import errors)
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", "ats_resume.db")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "ats_resume_db")

# RAG Configuration
RAG_VECTOR_STORE = os.getenv("RAG_VECTOR_STORE", "chroma")  # Options: "chroma", "faiss"
RAG_EMBEDDING_MODEL = os.getenv("RAG_EMBEDDING_MODEL", "text-embedding-ada-002")

# Application Configuration
APP_TITLE = "ATS Resume Scoring System"
APP_LAYOUT = "wide"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Scoring Configuration
DEFAULT_SKILLS_WEIGHT = 0.4
DEFAULT_EXPERIENCE_WEIGHT = 0.3
DEFAULT_EDUCATION_WEIGHT = 0.2
DEFAULT_FORMAT_WEIGHT = 0.1

# File Upload Configuration
ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]