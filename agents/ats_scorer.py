import re
from typing import Dict, List, Any, Optional
from utils.scoring_utils import calculate_category_score, normalize_score
from config import DEFAULT_SKILLS_WEIGHT, DEFAULT_EXPERIENCE_WEIGHT, DEFAULT_EDUCATION_WEIGHT, DEFAULT_FORMAT_WEIGHT

class ATSScorer:
    """
    Agent responsible for scoring resumes based on job description criteria.
    """
    
    def __init__(self):
        # Initialize scoring weights
        self.weights = {
            "skills": DEFAULT_SKILLS_WEIGHT,
            "experience": DEFAULT_EXPERIENCE_WEIGHT,
            "education": DEFAULT_EDUCATION_WEIGHT,
            "format": DEFAULT_FORMAT_WEIGHT
        }
        
        # Industry benchmarks (can be updated with RAG later)
        self.industry_benchmarks = {
            "technology": {
                "skills": 0.45,
                "experience": 0.35,
                "education": 0.15,
                "format": 0.05
            },
            "healthcare": {
                "skills": 0.30,
                "experience": 0.40,
                "education": 0.25,
                "format": 0.05
            },
            "finance": {
                "skills": 0.35,
                "experience": 0.35,
                "education": 0.25,
                "format": 0.05
            },
            "default": {
                "skills": DEFAULT_SKILLS_WEIGHT,
                "experience": DEFAULT_EXPERIENCE_WEIGHT,
                "education": DEFAULT_EDUCATION_WEIGHT,
                "format": DEFAULT_FORMAT_WEIGHT
            }
        }
    
    def score(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Score the resume against the job description.
        
        Args:
            resume_data (Dict[str, Any]): Structured resume data
            jd_data (Dict[str, Any]): Structured job description data
            
        Returns:
            Dict[str, Any]: Scoring results with breakdown
        """
        # Determine industry for appropriate benchmarks
        industry = jd_data.get("industry", "default")
        industry = industry.lower() if industry else "default"
        if industry not in self.industry_benchmarks:
            industry = "default"
        
        # Get industry-specific weights
        weights = self.industry_benchmarks[industry]
        
        # Calculate scores for each category
        skills_score = self._score_skills(resume_data, jd_data)
        experience_score = self._score_experience(resume_data, jd_data)
        education_score = self._score_education(resume_data, jd_data)
        format_score = self._score_format(resume_data)
        
        # Calculate weighted overall score
        overall_score = (
            skills_score * weights["skills"] +
            experience_score * weights["experience"] +
            education_score * weights["education"] +
            format_score * weights["format"]
        )
        
        # Normalize to 0-100 scale
        overall_score = normalize_score(overall_score)
        
        # Prepare score breakdown
        score_breakdown = {
            "skills": {
                "score": normalize_score(skills_score),
                "weight": weights["skills"],
                "details": self._get_skills_details(resume_data, jd_data)
            },
            "experience": {
                "score": normalize_score(experience_score),
                "weight": weights["experience"],
                "details": self._get_experience_details(resume_data, jd_data)
            },
            "education": {
                "score": normalize_score(education_score),
                "weight": weights["education"],
                "details": self._get_education_details(resume_data, jd_data)
            },
            "format": {
                "score": normalize_score(format_score),
                "weight": weights["format"],
                "details": self._get_format_details(resume_data)
            }
        }
        
        # Calculate confidence interval based on match strength
        confidence_interval = self._calculate_confidence_interval(score_breakdown)
        
        # Prepare final scoring results
        scoring_results = {
            "overall_score": overall_score,
            "score_breakdown": score_breakdown,
            "industry": industry,
            "weights": weights,
            "confidence_interval": confidence_interval,
            "benchmark": self._get_benchmark_comparison(overall_score, industry)
        }
        
        return scoring_results
    
    def _score_skills(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> float:
        """
        Score the skills match between resume and job description.
        
        Args:
            resume_data (Dict[str, Any]): Structured resume data
            jd_data (Dict[str, Any]): Structured job description data
            
        Returns:
            float: Skills score (0-1)
        """
        # Get skills from resume and job description, with null checks
        resume_skills = []
        for skill in resume_data.get("skills", []):
            if skill:  # Check if skill is not None or empty
                resume_skills.append(skill.lower())
        
        jd_required_skills = []
        for skill in jd_data.get("required_skills", []):
            if skill:  # Check if skill is not None or empty
                jd_required_skills.append(skill.lower())
        
        jd_preferred_skills = []
        for skill in jd_data.get("preferred_skills", []):
            if skill:  # Check if skill is not None or empty
                jd_preferred_skills.append(skill.lower())
        
        # Calculate required skills match
        required_matches = sum(1 for skill in jd_required_skills if skill in resume_skills)
        required_score = required_matches / len(jd_required_skills) if jd_required_skills else 1.0
        
        # Calculate preferred skills match
        preferred_matches = sum(1 for skill in jd_preferred_skills if skill in resume_skills)
        preferred_score = preferred_matches / len(jd_preferred_skills) if jd_preferred_skills else 1.0
        
        # Weighted combination (required skills are more important)
        skills_score = 0.7 * required_score + 0.3 * preferred_score
        
        return skills_score
    
    def _score_experience(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> float:
        """
        Score the experience match between resume and job description.
        
        Args:
            resume_data (Dict[str, Any]): Structured resume data
            jd_data (Dict[str, Any]): Structured job description data
            
        Returns:
            float: Experience score (0-1)
        """
        # Get experience from resume and job description
        resume_experience = resume_data.get("experience", [])
        jd_experience = jd_data.get("experience_requirements", {})
        
        # Calculate years of experience from resume
        total_years = 0
        for exp in resume_experience:
            duration = exp.get("duration", "") if exp.get("duration") else ""
            years = self._extract_years_from_duration(duration)
            total_years += years
        
        # Get required years from job description
        required_years = jd_experience.get("years", 0) if jd_experience.get("years") else 0
        
        # Calculate experience score based on years
        if required_years == 0:
            years_score = 1.0
        elif total_years >= required_years:
            years_score = 1.0
        else:
            years_score = total_years / required_years
        
        # Check for relevant experience
        relevant_experience = 0
        for exp in resume_experience:
            title = exp.get("title", "") if exp.get("title") else ""
            title = title.lower()
            
            description = exp.get("description", "") if exp.get("description") else ""
            description = description.lower()
            
            # Check if experience matches job requirements
            keywords = jd_experience.get("keywords", []) if jd_experience.get("keywords") else []
            if any(keyword in title or keyword in description for keyword in keywords):
                relevant_experience += 1
        
        relevance_score = relevant_experience / len(resume_experience) if resume_experience else 0
        
        # Combine years and relevance scores
        experience_score = 0.6 * years_score + 0.4 * relevance_score
        
        return experience_score
    
    def _score_education(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> float:
        """
        Score the education match between resume and job description.
        
        Args:
            resume_data (Dict[str, Any]): Structured resume data
            jd_data (Dict[str, Any]): Structured job description data
            
        Returns:
            float: Education score (0-1)
        """
        # Get education from resume and job description
        resume_education = resume_data.get("education", [])
        jd_education = jd_data.get("education_requirements", {})
        
        # If no education requirements, perfect score
        if not jd_education:
            return 1.0
        
        # Get required education level
        required_level = jd_education.get("level", "")
        required_level = required_level.lower() if required_level else ""
        
        # Get required fields
        fields = jd_education.get("fields", [])
        required_fields = [field.lower() if field else "" for field in fields]
        
        # Check if resume meets education requirements
        level_score = 0
        field_score = 0
        
        for edu in resume_education:
            # Check education level
            edu_level = edu.get("level", "")
            edu_level = edu_level.lower() if edu_level else ""
            
            if self._education_level_sufficient(edu_level, required_level):
                level_score = 1.0
                break
        
        # Check field of study
        if required_fields:
            for edu in resume_education:
                edu_field = edu.get("field", "")
                edu_field = edu_field.lower() if edu_field else ""
                
                if any(field in edu_field for field in required_fields):
                    field_score = 1.0
                    break
        else:
            field_score = 1.0
        
        # Combine level and field scores
        education_score = 0.7 * level_score + 0.3 * field_score
        
        return education_score
    
    def _score_format(self, resume_data: Dict[str, Any]) -> float:
        """
        Score the resume format and structure.
        
        Args:
            resume_data (Dict[str, Any]): Structured resume data
            
        Returns:
            float: Format score (0-1)
        """
        # Initialize format score
        format_score = 0.0
        
        # Check for presence of key sections
        sections = resume_data.get("sections", {})
        section_points = 0
        
        if "contact" in sections:
            section_points += 0.2
        if "summary" in sections:
            section_points += 0.2
        if "experience" in sections:
            section_points += 0.3
        if "education" in sections:
            section_points += 0.2
        if "skills" in sections:
            section_points += 0.1
        
        # Check for proper contact information
        contact_info = resume_data.get("contact_info", {})
        contact_points = 0
        
        if contact_info.get("email"):
            contact_points += 0.4
        if contact_info.get("phone"):
            contact_points += 0.4
        if contact_info.get("name"):
            contact_points += 0.2
        
        # Check for consistent formatting (heuristic)
        raw_text = resume_data.get("raw_text", "")
        consistency_points = 0
        
        # Check for consistent date formatting
        date_formats = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{4}/\d{1,2}/\d{1,2}',
            r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b'
        ]
        
        consistent_dates = False
        for date_format in date_formats:
            if len(re.findall(date_format, raw_text)) >= 2:
                consistent_dates = True
                break
        
        if consistent_dates:
            consistency_points += 0.5
        
        # Check for consistent section headers
        section_headers = [
            "Skills", "Experience", "Education", "Summary", "Contact"
        ]
        
        consistent_headers = False
        for header in section_headers:
            if header in raw_text:
                consistent_headers = True
                break
        
        if consistent_headers:
            consistency_points += 0.5
        
        # Calculate overall format score
        format_score = 0.4 * section_points + 0.4 * contact_points + 0.2 * consistency_points
        
        return format_score
    
    def _extract_years_from_duration(self, duration: str) -> float:
        """
        Extract years of experience from a duration string.
        
        Args:
            duration (str): Duration string (e.g., "2 years", "6 months")
            
        Returns:
            float: Years of experience
        """
        if not duration:
            return 0.0
        
        # Look for years
        years_match = re.search(r'(\d+)\s*(?:years?|yrs?)\b', duration, re.IGNORECASE)
        if years_match:
            return float(years_match.group(1))
        
        # Look for months
        months_match = re.search(r'(\d+)\s*months?\b', duration, re.IGNORECASE)
        if months_match:
            return float(months_match.group(1)) / 12
        
        return 0.0
    
    def _education_level_sufficient(self, candidate_level: str, required_level: str) -> bool:
        """
        Check if candidate's education level meets or exceeds required level.
        
        Args:
            candidate_level (str): Candidate's education level
            required_level (str): Required education level
            
        Returns:
            bool: True if candidate's level is sufficient
        """
        # Define education hierarchy
        education_hierarchy = [
            "high school", "associate", "bachelor", "master", "phd", "doctorate"
        ]
        
        # If either level is empty, return False
        if not candidate_level or not required_level:
            return False
        
        # Find positions in hierarchy
        try:
            candidate_pos = education_hierarchy.index(candidate_level)
            required_pos = education_hierarchy.index(required_level)
            return candidate_pos >= required_pos
        except ValueError:
            return False
    
    def _calculate_confidence_interval(self, score_breakdown: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate confidence interval for the overall score.
        
        Args:
            score_breakdown (Dict[str, Any]): Score breakdown by category
            
        Returns:
            Dict[str, float]: Confidence interval (lower, upper)
        """
        # Calculate variance based on category scores
        scores = [details["score"] for details in score_breakdown.values()]
        weights = [details["weight"] for details in score_breakdown.values()]
        
        # Calculate weighted variance
        weighted_scores = [score * weight for score, weight in zip(scores, weights)]
        mean_score = sum(weighted_scores) / sum(weights)
        variance = sum(weight * (score - mean_score) ** 2 for score, weight in zip(scores, weights)) / sum(weights)
        std_dev = variance ** 0.5
        
        # Calculate 95% confidence interval
        margin = 1.96 * std_dev
        lower = max(0, mean_score - margin)
        upper = min(100, mean_score + margin)
        
        return {"lower": lower, "upper": upper}
    
    def _get_benchmark_comparison(self, score: float, industry: str) -> Dict[str, Any]:
        """
        Compare score against industry benchmarks.
        
        Args:
            score (float): Resume score
            industry (str): Industry name
            
        Returns:
            Dict[str, Any]: Benchmark comparison data
        """
        # Industry benchmarks (these would ideally come from RAG)
        industry_benchmarks = {
            "technology": {"average": 75, "top": 90},
            "healthcare": {"average": 70, "top": 85},
            "finance": {"average": 72, "top": 88},
            "default": {"average": 65, "top": 80}
        }
        
        benchmark = industry_benchmarks.get(industry, industry_benchmarks["default"])
        
        # Calculate percentile
        if score >= benchmark["top"]:
            percentile = 90
        elif score >= benchmark["average"]:
            percentile = 50 + 40 * ((score - benchmark["average"]) / (benchmark["top"] - benchmark["average"]))
        else:
            percentile = 50 * (score / benchmark["average"])
        
        return {
            "industry": industry,
            "score": score,
            "average": benchmark["average"],
            "top": benchmark["top"],
            "percentile": percentile
        }
    
    def _get_skills_details(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed skills matching information."""
        # Get skills with null checks
        resume_skills = []
        for skill in resume_data.get("skills", []):
            if skill:  # Check if skill is not None or empty
                resume_skills.append(skill.lower())
        
        jd_required_skills = []
        for skill in jd_data.get("required_skills", []):
            if skill:  # Check if skill is not None or empty
                jd_required_skills.append(skill.lower())
        
        jd_preferred_skills = []
        for skill in jd_data.get("preferred_skills", []):
            if skill:  # Check if skill is not None or empty
                jd_preferred_skills.append(skill.lower())
        
        # Find matches and gaps
        required_matches = [skill for skill in jd_required_skills if skill in resume_skills]
        required_gaps = [skill for skill in jd_required_skills if skill not in resume_skills]
        preferred_matches = [skill for skill in jd_preferred_skills if skill in resume_skills]
        preferred_gaps = [skill for skill in jd_preferred_skills if skill not in resume_skills]
        
        return {
            "required_matches": required_matches,
            "required_gaps": required_gaps,
            "preferred_matches": preferred_matches,
            "preferred_gaps": preferred_gaps
        }
    
    def _get_experience_details(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed experience matching information."""
        resume_experience = resume_data.get("experience", [])
        jd_experience = jd_data.get("experience_requirements", {})
        
        # Calculate years of experience
        total_years = 0
        for exp in resume_experience:
            duration = exp.get("duration", "") if exp.get("duration") else ""
            years = self._extract_years_from_duration(duration)
            total_years += years
        
        required_years = jd_experience.get("years", 0) if jd_experience.get("years") else 0
        
        # Check for relevant experience
        relevant_experience = []
        for exp in resume_experience:
            title = exp.get("title", "") if exp.get("title") else ""
            title = title.lower()
            
            description = exp.get("description", "") if exp.get("description") else ""
            description = description.lower()
            
            keywords = jd_experience.get("keywords", []) if jd_experience.get("keywords") else []
            if any(keyword in title or keyword in description for keyword in keywords):
                relevant_experience.append(exp.get("title", "") if exp.get("title") else "")
        
        return {
            "total_years": total_years,
            "required_years": required_years,
            "relevant_experience": relevant_experience
        }
    
    def _get_education_details(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed education matching information."""
        resume_education = resume_data.get("education", [])
        jd_education = jd_data.get("education_requirements", {})
        
        # Check education level
        required_level = jd_education.get("level", "")
        required_level = required_level.lower() if required_level else ""
        
        level_met = False
        
        for edu in resume_education:
            edu_level = edu.get("level", "")
            edu_level = edu_level.lower() if edu_level else ""
            
            if self._education_level_sufficient(edu_level, required_level):
                level_met = True
                break
        
        # Check field of study
        fields = jd_education.get("fields", [])
        required_fields = [field.lower() if field else "" for field in fields]
        
        field_met = False
        
        if required_fields:
            for edu in resume_education:
                edu_field = edu.get("field", "")
                edu_field = edu_field.lower() if edu_field else ""
                
                if any(field in edu_field for field in required_fields):
                    field_met = True
                    break
        else:
            field_met = True
        
        return {
            "level_met": level_met,
            "field_met": field_met,
            "required_level": required_level,
            "required_fields": required_fields
        }
    
    def _get_format_details(self, resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed format evaluation information."""
        sections = resume_data.get("sections", {})
        contact_info = resume_data.get("contact_info", {})
        
        # Check sections
        section_status = {
            "contact": "contact" in sections,
            "summary": "summary" in sections,
            "experience": "experience" in sections,
            "education": "education" in sections,
            "skills": "skills" in sections
        }
        
        # Check contact info
        contact_status = {
            "email": bool(contact_info.get("email")),
            "phone": bool(contact_info.get("phone")),
            "name": bool(contact_info.get("name"))
        }
        
        return {
            "sections": section_status,
            "contact": contact_status
        }