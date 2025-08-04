from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

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
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'resume_data': self.resume_data,
            'jd_data': self.jd_data,
            'score_data': self.score_data,
            'recommendations': self.recommendations,
            'overall_score': self.overall_score,
            'user_session': self.user_session
        }