import os
from typing import Any
from pymongo import MongoClient
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DB_TYPE, SQLITE_DB_PATH, MONGO_URI, MONGO_DB_NAME

Base = declarative_base()

class ResumeScoringResult(Base):
    """SQLAlchemy model for resume scoring results."""
    __tablename__ = 'resume_scoring_results'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    resume_data = Column(Text)  # JSON string
    jd_data = Column(Text)  # JSON string
    score_data = Column(Text)  # JSON string
    recommendations = Column(Text)  # JSON string
    overall_score = Column(Float)
    user_session = Column(String(255))

class DatabaseConnection:
    """Database connection manager."""
    
    def __init__(self):
        self.db_type = DB_TYPE
        self.connection = None
        self.engine = None
        self.session = None
        
        if self.db_type == "sqlite":
            self._setup_sqlite()
        elif self.db_type == "mongodb":
            self._setup_mongodb()
    
    def _setup_sqlite(self):
        """Setup SQLite database connection."""
        self.engine = create_engine(f'sqlite:///{SQLITE_DB_PATH}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def _setup_mongodb(self):
        """Setup MongoDB database connection."""
        client = MongoClient(MONGO_URI)
        self.connection = client[MONGO_DB_NAME]
    
    def get_connection(self):
        """Get the database connection."""
        if self.db_type == "sqlite":
            return self.session
        elif self.db_type == "mongodb":
            return self.connection
    
    def close(self):
        """Close the database connection."""
        if self.db_type == "sqlite" and self.session:
            self.session.close()
        elif self.db_type == "mongodb" and self.connection:
            self.connection.client.close()