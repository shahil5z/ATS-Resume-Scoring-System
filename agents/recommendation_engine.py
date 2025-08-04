from typing import Dict, List, Any, Optional
from utils.text_processing import clean_text

class RecommendationEngine:
    """
    Agent responsible for generating improvement recommendations for resumes.
    """
    
    def __init__(self):
        # Initialize recommendation templates
        self.recommendation_templates = {
            "skills_gap": {
                "title": "Skills Gap",
                "description": "Your resume is missing some key skills mentioned in the job description.",
                "suggestions": [
                    "Consider adding these skills to your resume if you have them: {missing_skills}",
                    "If you don't have these skills, consider taking online courses or certifications to acquire them.",
                    "Highlight transferable skills that are similar to the required skills."
                ]
            },
            "experience_gap": {
                "title": "Experience Gap",
                "description": "Your experience doesn't fully match the job requirements.",
                "suggestions": [
                    "Emphasize relevant projects or achievements that demonstrate the required experience.",
                    "Quantify your accomplishments with metrics and results.",
                    "Consider gaining more experience in the required areas through freelance work or personal projects."
                ]
            },
            "education_gap": {
                "title": "Education Gap",
                "description": "Your education qualifications don't fully match the job requirements.",
                "suggestions": [
                    "Highlight relevant coursework, projects, or certifications.",
                    "Emphasize your practical experience to compensate for education gaps.",
                    "Consider pursuing additional education or certifications if possible."
                ]
            },
            "format_issues": {
                "title": "Resume Format Issues",
                "description": "Your resume could be improved in terms of formatting and structure.",
                "suggestions": [
                    "Ensure your resume has all the standard sections: Contact, Summary, Experience, Education, Skills.",
                    "Use consistent formatting throughout your resume.",
                    "Keep your resume to 1-2 pages maximum.",
                    "Use bullet points to make your experience easy to scan.",
                    "Use a professional font and appropriate spacing."
                ]
            },
            "keyword_optimization": {
                "title": "Keyword Optimization",
                "description": "Your resume could be better optimized for ATS systems.",
                "suggestions": [
                    "Include keywords from the job description throughout your resume.",
                    "Use variations of keywords (e.g., 'managed' and 'management').",
                    "Place important keywords in prominent positions like the summary and skills section.",
                    "Avoid graphics, tables, and special characters that ATS systems might not parse correctly."
                ]
            }
        }
    
    def generate_recommendations(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any], score_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate improvement recommendations for the resume.
        
        Args:
            resume_data (Dict[str, Any]): Structured resume data
            jd_data (Dict[str, Any]): Structured job description data
            score_data (Dict[str, Any]): Scoring results
            
        Returns:
            List[Dict[str, Any]]: List of recommendations
        """
        recommendations = []
        
        # Get score breakdown
        score_breakdown = score_data.get("score_breakdown", {})
        
        # Generate skills gap recommendations
        skills_score = score_breakdown.get("skills", {}).get("score", 0)
        if skills_score < 0.8:
            skills_details = score_breakdown.get("skills", {}).get("details", {})
            missing_skills = skills_details.get("required_gaps", []) + skills_details.get("preferred_gaps", [])
            
            if missing_skills:
                recommendation = self._create_recommendation(
                    "skills_gap",
                    {"missing_skills": ", ".join(missing_skills[:5])}  # Limit to top 5
                )
                recommendations.append(recommendation)
        
        # Generate experience gap recommendations
        experience_score = score_breakdown.get("experience", {}).get("score", 0)
        if experience_score < 0.8:
            experience_details = score_breakdown.get("experience", {}).get("details", {})
            total_years = experience_details.get("total_years", 0)
            required_years = experience_details.get("required_years", 0)
            
            if total_years < required_years:
                recommendation = self._create_recommendation(
                    "experience_gap",
                    {"years_shortfall": required_years - total_years}
                )
                recommendations.append(recommendation)
        
        # Generate education gap recommendations
        education_score = score_breakdown.get("education", {}).get("score", 0)
        if education_score < 0.8:
            education_details = score_breakdown.get("education", {}).get("details", {})
            
            if not education_details.get("level_met", False) or not education_details.get("field_met", False):
                recommendation = self._create_recommendation("education_gap", {})
                recommendations.append(recommendation)
        
        # Generate format recommendations
        format_score = score_breakdown.get("format", {}).get("score", 0)
        if format_score < 0.9:
            format_details = score_breakdown.get("format", {}).get("details", {})
            
            # Check for missing sections
            missing_sections = [section for section, present in format_details.get("sections", {}).items() if not present]
            missing_contact = [field for field, present in format_details.get("contact", {}).items() if not present]
            
            if missing_sections or missing_contact:
                recommendation = self._create_recommendation(
                    "format_issues",
                    {"missing_sections": missing_sections, "missing_contact": missing_contact}
                )
                recommendations.append(recommendation)
        
        # Generate keyword optimization recommendations
        overall_score = score_data.get("overall_score", 0)
        if overall_score < 70:
            recommendation = self._create_recommendation("keyword_optimization", {})
            recommendations.append(recommendation)
        
        # Generate specific content recommendations
        content_recommendations = self._generate_content_recommendations(resume_data, jd_data)
        recommendations.extend(content_recommendations)
        
        # Sort recommendations by priority (lower score = higher priority)
        recommendations.sort(key=lambda x: x.get("priority", 0))
        
        return recommendations
    
    def _create_recommendation(self, template_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a recommendation from a template.
        
        Args:
            template_name (str): Name of the recommendation template
            context (Dict[str, Any]): Context for the recommendation
            
        Returns:
            Dict[str, Any]: Formatted recommendation
        """
        template = self.recommendation_templates.get(template_name, {})
        
        # Format suggestions with context, handling None values
        suggestions = []
        for suggestion in template.get("suggestions", []):
            try:
                # Replace None values in context with empty strings
                safe_context = {k: v if v is not None else "" for k, v in context.items()}
                formatted_suggestion = suggestion.format(**safe_context)
                suggestions.append(formatted_suggestion)
            except KeyError:
                suggestions.append(suggestion)
        
        # Determine priority based on template
        priority_map = {
            "skills_gap": 1,
            "experience_gap": 2,
            "education_gap": 3,
            "format_issues": 4,
            "keyword_optimization": 5
        }
        
        recommendation = {
            "title": template.get("title", ""),
            "description": template.get("description", ""),
            "suggestions": suggestions,
            "priority": priority_map.get(template_name, 10),
            "category": template_name
        }
        
        return recommendation
    
    def _generate_content_recommendations(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate specific content recommendations for the resume.
        
        Args:
            resume_data (Dict[str, Any]): Structured resume data
            jd_data (Dict[str, Any]): Structured job description data
            
        Returns:
            List[Dict[str, Any]]: List of content recommendations
        """
        recommendations = []
        
        # Check for missing summary
        if not resume_data.get("summary"):
            recommendation = {
                "title": "Missing Professional Summary",
                "description": "Your resume doesn't have a professional summary section.",
                "suggestions": [
                    "Add a professional summary at the top of your resume (2-3 sentences).",
                    "Highlight your most relevant skills and experience for this job.",
                    "Include keywords from the job description in your summary."
                ],
                "priority": 3,
                "category": "content"
            }
            recommendations.append(recommendation)
        
        # Check for weak experience descriptions
        experience = resume_data.get("experience", [])
        weak_experience = []
        
        for exp in experience:
            description = exp.get("description", "")
            if len(description) < 50 or not any(char.isdigit() for char in description):
                weak_experience.append(exp.get("title", ""))
        
        if weak_experience:
            recommendation = {
                "title": "Weak Experience Descriptions",
                "description": "Some of your experience descriptions could be more detailed and impactful.",
                "suggestions": [
                    f"Strengthen descriptions for these roles: {', '.join(weak_experience)}",
                    "Use action verbs to start bullet points (e.g., 'Managed', 'Developed', 'Implemented').",
                    "Quantify your achievements with numbers, percentages, and results.",
                    "Focus on accomplishments rather than just responsibilities."
                ],
                "priority": 4,
                "category": "content"
            }
            recommendations.append(recommendation)
        
        # Check for skills presentation
        skills = resume_data.get("skills", [])
        if len(skills) < 5:
            recommendation = {
                "title": "Insufficient Skills Section",
                "description": "Your skills section could be more comprehensive.",
                "suggestions": [
                    "Add more relevant skills to your skills section.",
                    "Include both technical and soft skills.",
                    "Organize skills into categories (e.g., Technical Skills, Soft Skills).",
                    "Include skills mentioned in the job description."
                ],
                "priority": 2,
                "category": "content"
            }
            recommendations.append(recommendation)
        
        return recommendations