import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from database.connection import DatabaseConnection, ResumeScoringResult

class DatabaseOperations:
    """Database operations for resume scoring system."""
    
    def __init__(self):
        self.db_connection = DatabaseConnection()
        self.db = self.db_connection.get_connection()
        self.db_type = self.db_connection.db_type
    
    def save_scoring_result(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any], 
                           score_data: Dict[str, Any], recommendations: List[Dict[str, Any]],
                           user_session: str = None) -> str:
        """
        Save a resume scoring result to the database.
        
        Args:
            resume_data (Dict[str, Any]): Structured resume data
            jd_data (Dict[str, Any]): Structured job description data
            score_data (Dict[str, Any]): Scoring results
            recommendations (List[Dict[str, Any]]): List of recommendations
            user_session (str, optional): User session identifier
            
        Returns:
            str: ID of the saved record
        """
        if self.db_type == "sqlite":
            return self._save_sqlite(resume_data, jd_data, score_data, recommendations, user_session)
        elif self.db_type == "mongodb":
            return self._save_mongodb(resume_data, jd_data, score_data, recommendations, user_session)
    
    def _save_sqlite(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any], 
                    score_data: Dict[str, Any], recommendations: List[Dict[str, Any]],
                    user_session: str = None) -> str:
        """Save scoring result to SQLite database."""
        # Create new record
        record = ResumeScoringResult(
            resume_data=json.dumps(resume_data),
            jd_data=json.dumps(jd_data),
            score_data=json.dumps(score_data),
            recommendations=json.dumps(recommendations),
            overall_score=score_data.get("overall_score", 0),
            user_session=user_session
        )
        
        # Add to database
        self.db.add(record)
        self.db.commit()
        
        return str(record.id)
    
    def _save_mongodb(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any], 
                     score_data: Dict[str, Any], recommendations: List[Dict[str, Any]],
                     user_session: str = None) -> str:
        """Save scoring result to MongoDB database."""
        # Create document
        document = {
            "timestamp": datetime.utcnow(),
            "resume_data": resume_data,
            "jd_data": jd_data,
            "score_data": score_data,
            "recommendations": recommendations,
            "overall_score": score_data.get("overall_score", 0),
            "user_session": user_session
        }
        
        # Insert into collection
        result = self.db.scoring_results.insert_one(document)
        
        return str(result.inserted_id)
    
    def get_scoring_history(self, user_session: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get scoring history from the database.
        
        Args:
            user_session (str, optional): User session identifier
            limit (int): Maximum number of records to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of scoring records
        """
        if self.db_type == "sqlite":
            return self._get_sqlite_history(user_session, limit)
        elif self.db_type == "mongodb":
            return self._get_mongodb_history(user_session, limit)
    
    def _get_sqlite_history(self, user_session: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get scoring history from SQLite database."""
        query = self.db.query(ResumeScoringResult)
        
        if user_session:
            query = query.filter(ResumeScoringResult.user_session == user_session)
        
        records = query.order_by(ResumeScoringResult.timestamp.desc()).limit(limit).all()
        
        return [record.to_dict() for record in records]
    
    def _get_mongodb_history(self, user_session: str = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Get scoring history from MongoDB database."""
        query = {}
        
        if user_session:
            query["user_session"] = user_session
        
        cursor = self.db.scoring_results.find(query).sort("timestamp", -1).limit(limit)
        
        records = []
        for record in cursor:
            record["_id"] = str(record["_id"])
            records.append(record)
        
        return records
    
    def get_scoring_result(self, result_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific scoring result by ID.
        
        Args:
            result_id (str): ID of the scoring result
            
        Returns:
            Optional[Dict[str, Any]]: Scoring result or None if not found
        """
        if self.db_type == "sqlite":
            return self._get_sqlite_result(result_id)
        elif self.db_type == "mongodb":
            return self._get_mongodb_result(result_id)
    
    def _get_sqlite_result(self, result_id: str) -> Optional[Dict[str, Any]]:
        """Get scoring result from SQLite database."""
        record = self.db.query(ResumeScoringResult).filter(ResumeScoringResult.id == int(result_id)).first()
        
        if record:
            return record.to_dict()
        return None
    
    def _get_mongodb_result(self, result_id: str) -> Optional[Dict[str, Any]]:
        """Get scoring result from MongoDB database."""
        from bson.objectid import ObjectId
        
        record = self.db.scoring_results.find_one({"_id": ObjectId(result_id)})
        
        if record:
            record["_id"] = str(record["_id"])
            return record
        return None
    
    def delete_scoring_result(self, result_id: str) -> bool:
        """
        Delete a scoring result by ID.
        
        Args:
            result_id (str): ID of the scoring result
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.db_type == "sqlite":
            return self._delete_sqlite_result(result_id)
        elif self.db_type == "mongodb":
            return self._delete_mongodb_result(result_id)
    
    def _delete_sqlite_result(self, result_id: str) -> bool:
        """Delete scoring result from SQLite database."""
        record = self.db.query(ResumeScoringResult).filter(ResumeScoringResult.id == int(result_id)).first()
        
        if record:
            self.db.delete(record)
            self.db.commit()
            return True
        return False
    
    def _delete_mongodb_result(self, result_id: str) -> bool:
        """Delete scoring result from MongoDB database."""
        from bson.objectid import ObjectId
        
        result = self.db.scoring_results.delete_one({"_id": ObjectId(result_id)})
        
        return result.deleted_count > 0
    
    def close(self):
        """Close the database connection."""
        self.db_connection.close()