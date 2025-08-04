import re
from typing import Dict, List, Any, Optional
import spacy
from utils.text_processing import clean_text

class JDAnalyzer:
    """
    Agent responsible for analyzing job descriptions and extracting requirements.
    """
    
    def __init__(self):
        # Load spaCy model for NLP tasks
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # Fallback to a smaller model if the main one isn't available
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        
        # Define patterns for extracting specific information
        self.years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\b'
        self.education_pattern = r'\b(?:Bachelor|Master|PhD|Doctorate|Associate|High School|Degree|Diploma|B\.S\.|M\.S\.|B\.A\.|M\.A\.|BSc|MSc|BA|MA)\b'
        
        # Extended skill keywords for extraction
        self.skill_keywords = [
            # Programming Languages
            "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin",
            "Go", "Rust", "Scala", "R", "MATLAB", "Perl", "Shell", "Bash", "PowerShell",
            
            # Web Development
            "HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Express", "Django", "Flask",
            "ASP.NET", "Spring", "Ruby on Rails", "Laravel", "Symfony", "jQuery", "Bootstrap",
            "Next.js", "Nuxt.js", "Svelte", "Gatsby", "Ember.js", "Backbone.js",
            
            # Databases
            "SQL", "MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQLite", "Redis", "Cassandra",
            "DynamoDB", "Firebase", "Elasticsearch", "GraphQL", "MariaDB", "CouchDB",
            
            # Data Science & AI
            "Machine Learning", "Deep Learning", "Data Science", "Data Analysis", "Statistics",
            "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy", "NLTK",
            "Computer Vision", "NLP", "Big Data", "Hadoop", "Spark", "Tableau", "Power BI",
            "Jupyter", "Kaggle", "Data Visualization", "Predictive Modeling", "Statistical Analysis",
            
            # DevOps & Cloud
            "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "Git",
            "CI/CD", "Terraform", "Ansible", "Linux", "Unix", "Networking", "Security",
            "Microservices", "Serverless", "DevOps", "Agile", "Scrum", "Kanban",
            
            # Project Management
            "Project Management", "PMP", "Agile", "Scrum", "Kanban", "Waterfall", "JIRA",
            "Trello", "Asana", "Risk Management", "Budgeting", "Planning", "Team Leadership",
            
            # Soft Skills
            "Leadership", "Communication", "Teamwork", "Problem Solving", "Critical Thinking",
            "Time Management", "Creativity", "Adaptability", "Collaboration", "Emotional Intelligence",
            "Public Speaking", "Negotiation", "Conflict Resolution", "Decision Making", "Interpersonal Skills"
        ]
        
        # Industry keywords
        self.industry_keywords = {
            "technology": ["software", "developer", "engineer", "IT", "technical", "programming", "data", "cloud"],
            "healthcare": ["medical", "health", "patient", "clinical", "nurse", "doctor", "healthcare"],
            "finance": ["financial", "banking", "investment", "accounting", "finance", "economics", "fintech"],
            "education": ["teaching", "education", "school", "university", "learning", "academic", "training"],
            "retail": ["sales", "retail", "customer", "store", "shop", "merchandise", "e-commerce"],
            "manufacturing": ["production", "manufacturing", "factory", "industrial", "plant", "logistics"],
            "consulting": ["consulting", "consultant", "advisory", "strategy", "client", "professional services"]
        }
        
        # Section patterns
        self.section_patterns = {
            "responsibilities": r"(?i)(responsibilities|duties|what you'll do|role|job duties|key responsibilities)",
            "qualifications": r"(?i)(qualifications|requirements|what we're looking for|skills required|candidate profile)",
            "experience": r"(?i)(experience|work experience|professional experience|required experience)",
            "education": r"(?i)(education|educational requirements|academic|degree|qualification)",
            "skills": r"(?i)(skills|technical skills|required skills|preferred skills|technologies)"
        }
    
    def analyze(self, jd_text: str) -> Dict[str, Any]:
        """
        Analyze the job description text and extract requirements.
        
        Args:
            jd_text (str): Raw text extracted from the job description file
            
        Returns:
            Dict[str, Any]: Structured job description data
        """
        # Clean the text
        cleaned_text = clean_text(jd_text)
        
        # Extract job title
        job_title = self._extract_job_title(cleaned_text)
        
        # Extract company name
        company = self._extract_company(cleaned_text)
        
        # Extract industry
        industry = self._extract_industry(cleaned_text)
        
        # Extract required skills
        required_skills = self._extract_required_skills(cleaned_text)
        
        # Extract preferred skills
        preferred_skills = self._extract_preferred_skills(cleaned_text)
        
        # Extract experience requirements
        experience_requirements = self._extract_experience_requirements(cleaned_text)
        
        # Extract education requirements
        education_requirements = self._extract_education_requirements(cleaned_text)
        
        # Extract responsibilities
        responsibilities = self._extract_responsibilities(cleaned_text)
        
        # Extract qualifications
        qualifications = self._extract_qualifications(cleaned_text)
        
        # Construct the structured job description data
        jd_data = {
            "job_title": job_title,
            "company": company,
            "industry": industry,
            "required_skills": required_skills,
            "preferred_skills": preferred_skills,
            "experience_requirements": experience_requirements,
            "education_requirements": education_requirements,
            "responsibilities": responsibilities,
            "qualifications": qualifications,
            "raw_text": cleaned_text
        }
        
        return jd_data
    
    def _extract_job_title(self, text: str) -> Optional[str]:
        """Extract the job title from the job description text."""
        # The job title is typically at the beginning of the description
        first_lines = text.split('\n')[:5]
        
        # Process each line with spaCy to find potential job titles
        for line in first_lines:
            doc = self.nlp(line)
            for token in doc:
                # Look for common job title patterns
                if token.pos_ == "NOUN" and token.text[0].isupper():
                    # Check if it's a common job title pattern
                    if any(pattern in line.lower() for pattern in ["engineer", "developer", "manager", "analyst", "specialist", "coordinator", "director", "lead", "head", "chief"]):
                        return line.strip()
        
        # Fallback: Look for job title patterns in the entire text
        job_title_patterns = [
            r'(Job Title|Position|Role):\s*([^\n]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Engineer|Developer|Manager|Analyst|Specialist|Coordinator|Director|Lead|Head|Chief))',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:I|II|III|IV|V|Jr|Sr))'
        ]
        
        for pattern in job_title_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # Return the last group (the job title)
                return match.group(-1).strip()
        
        return None
    
    def _extract_company(self, text: str) -> Optional[str]:
        """Extract the company name from the job description text."""
        # Look for company indicators
        company_indicators = ["company:", "organization:", "at", "with", "join"]
        
        for indicator in company_indicators:
            pattern = rf'{indicator}\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        # Look for company names in the first few lines
        first_lines = text.split('\n')[:3]
        for line in first_lines:
            # Look for capitalized words that might be company names
            words = line.split()
            for i in range(len(words) - 1):
                if words[i][0].isupper() and words[i+1][0].isupper():
                    potential_company = f"{words[i]} {words[i+1]}"
                    # Check if it's likely a company name (not a job title)
                    if not any(pattern in potential_company.lower() for pattern in ["job description", "position", "role", "title"]):
                        return potential_company
        
        return None
    
    def _extract_industry(self, text: str) -> str:
        """Extract the industry from the job description text."""
        text_lower = text.lower()
        
        # Check for industry keywords
        for industry, keywords in self.industry_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return industry
        
        return "default"
    
    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills from the job description text."""
        required_skills = []
        
        # Look for required skills section
        required_section = self._extract_section(text, ["required skills", "must have", "qualifications", "requirements", "skills needed"])
        
        if required_section:
            # Extract skills based on predefined keywords
            for skill in self.skill_keywords:
                if re.search(r'\b' + re.escape(skill) + r'\b', required_section, re.IGNORECASE):
                    required_skills.append(skill)
            
            # Extract skills using NLP
            doc = self.nlp(required_section)
            
            # Look for noun phrases that might indicate skills
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.strip()
                
                # Check if the chunk is a skill (heuristic: 2-4 words, starts with capital letter)
                if chunk_text and 2 <= len(chunk_text.split()) <= 4 and chunk_text[0].isupper():
                    if chunk_text not in required_skills:
                        required_skills.append(chunk_text)
            
            # Look for bullet points that might contain skills
            bullet_patterns = [
                r'•\s*([^•\n]+)',
                r'-\s*([^\-\n]+)',
                r'\*\s*([^\\\n]+)',
                r'\d+\.\s*([^\n]+)'
            ]
            
            for pattern in bullet_patterns:
                matches = re.findall(pattern, required_section)
                for match in matches:
                    # Clean the match
                    skill = match.strip()
                    if skill and skill not in required_skills:
                        required_skills.append(skill)
        else:
            # If no specific section, look for skills in the entire text
            for skill in self.skill_keywords:
                if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
                    required_skills.append(skill)
        
        # Remove duplicates and empty skills
        required_skills = list(set(skill for skill in required_skills if skill.strip()))
        
        return required_skills
    
    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract preferred skills from the job description text."""
        preferred_skills = []
        
        # Look for preferred skills section
        preferred_section = self._extract_section(text, ["preferred skills", "nice to have", "plus", "bonus", "advantageous"])
        
        if preferred_section:
            # Extract skills based on predefined keywords
            for skill in self.skill_keywords:
                if re.search(r'\b' + re.escape(skill) + r'\b', preferred_section, re.IGNORECASE):
                    preferred_skills.append(skill)
            
            # Extract skills using NLP
            doc = self.nlp(preferred_section)
            
            # Look for noun phrases that might indicate skills
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.strip()
                
                # Check if the chunk is a skill (heuristic: 2-4 words, starts with capital letter)
                if chunk_text and 2 <= len(chunk_text.split()) <= 4 and chunk_text[0].isupper():
                    if chunk_text not in preferred_skills:
                        preferred_skills.append(chunk_text)
            
            # Look for bullet points that might contain skills
            bullet_patterns = [
                r'•\s*([^•\n]+)',
                r'-\s*([^\-\n]+)',
                r'\*\s*([^\\\n]+)',
                r'\d+\.\s*([^\n]+)'
            ]
            
            for pattern in bullet_patterns:
                matches = re.findall(pattern, preferred_section)
                for match in matches:
                    # Clean the match
                    skill = match.strip()
                    if skill and skill not in preferred_skills:
                        preferred_skills.append(skill)
        
        # Remove duplicates and empty skills
        preferred_skills = list(set(skill for skill in preferred_skills if skill.strip()))
        
        return preferred_skills
    
    def _extract_experience_requirements(self, text: str) -> Dict[str, Any]:
        """Extract experience requirements from the job description text."""
        # Extract years of experience
        years_match = re.search(self.years_pattern, text)
        years = int(years_match.group(1)) if years_match else 0
        
        # Extract experience keywords
        experience_keywords = []
        doc = self.nlp(text)
        
        # Look for experience-related terms
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN"] and token.text[0].isupper():
                # Check if it's related to experience
                if any(pattern in token.text.lower() for pattern in ["experience", "work", "project", "role"]):
                    experience_keywords.append(token.text)
        
        # Extract specific experience requirements
        experience_requirements = {
            "years": years,
            "keywords": experience_keywords
        }
        
        return experience_requirements
    
    def _extract_education_requirements(self, text: str) -> Dict[str, Any]:
        """Extract education requirements from the job description text."""
        # Extract education level
        education_level = None
        education_matches = re.findall(self.education_pattern, text, re.IGNORECASE)
        
        if education_matches:
            # Determine the highest education level mentioned
            levels = ["High School", "Associate", "Bachelor", "Master", "PhD", "Doctorate"]
            for level in reversed(levels):
                if any(level.lower() in match.lower() for match in education_matches):
                    education_level = level
                    break
        
        # Extract fields of study
        fields = []
        doc = self.nlp(text)
        
        # Look for field-related terms
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.strip()
            
            # Check if it's a field of study (heuristic: contains "in", "of", "related to")
            if any(indicator in chunk_text.lower() for indicator in [" in ", " of ", "related to"]):
                # Extract the field name
                field_match = re.search(r'(?:in|of|related to)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', chunk_text, re.IGNORECASE)
                if field_match:
                    field = field_match.group(1).strip()
                    if field not in fields:
                        fields.append(field)
        
        education_requirements = {
            "level": education_level,
            "fields": fields
        }
        
        return education_requirements
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract responsibilities from the job description text."""
        responsibilities = []
        
        # Look for responsibilities section
        responsibilities_section = self._extract_section(text, ["responsibilities", "duties", "what you'll do", "role"])
        
        if responsibilities_section:
            # Split into bullet points or sentences
            bullet_patterns = [
                r'•\s*([^•\n]+)',
                r'-\s*([^\-\n]+)',
                r'\*\s*([^\\\n]+)',
                r'\d+\.\s*([^\n]+)'
            ]
            
            # Try to extract bullet points first
            found_bullets = False
            for pattern in bullet_patterns:
                matches = re.findall(pattern, responsibilities_section)
                if matches:
                    found_bullets = True
                    for match in matches:
                        responsibility = match.strip()
                        if responsibility and len(responsibility) > 10:  # Filter out very short items
                            responsibilities.append(responsibility)
            
            # If no bullet points found, split by sentences
            if not found_bullets:
                sentences = re.split(r'\.\s+', responsibilities_section)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence and len(sentence) > 10:  # Filter out very short sentences
                        responsibilities.append(sentence)
        
        return responsibilities
    
    def _extract_qualifications(self, text: str) -> List[str]:
        """Extract qualifications from the job description text."""
        qualifications = []
        
        # Look for qualifications section
        qualifications_section = self._extract_section(text, ["qualifications", "requirements", "what we're looking for", "skills required"])
        
        if qualifications_section:
            # Split into bullet points or sentences
            bullet_patterns = [
                r'•\s*([^•\n]+)',
                r'-\s*([^\-\n]+)',
                r'\*\s*([^\\\n]+)',
                r'\d+\.\s*([^\n]+)'
            ]
            
            # Try to extract bullet points first
            found_bullets = False
            for pattern in bullet_patterns:
                matches = re.findall(pattern, qualifications_section)
                if matches:
                    found_bullets = True
                    for match in matches:
                        qualification = match.strip()
                        if qualification and len(qualification) > 10:  # Filter out very short items
                            qualifications.append(qualification)
            
            # If no bullet points found, split by sentences
            if not found_bullets:
                sentences = re.split(r'\.\s+', qualifications_section)
                for sentence in sentences:
                    sentence = sentence.strip()
                    if sentence and len(sentence) > 10:  # Filter out very short sentences
                        qualifications.append(sentence)
        
        return qualifications
    
    def _extract_section(self, text: str, section_headers: List[str]) -> Optional[str]:
        """Extract a specific section from the job description text."""
        # Find the position of each section header
        section_positions = {}
        
        for header in section_headers:
            pattern = rf'(?i)\b{re.escape(header)}\b'
            matches = list(re.finditer(pattern, text))
            if matches:
                section_positions[header] = matches[0].start()
        
        if not section_positions:
            return None
        
        # Find the earliest section header
        first_header = min(section_positions, key=section_positions.get)
        start_pos = section_positions[first_header]
        
        # Find the end of the section (next section header or end of text)
        end_pos = len(text)
        for header in section_headers:
            if header != first_header:
                pattern = rf'(?i)\b{re.escape(header)}\b'
                matches = list(re.finditer(pattern, text))
                for match in matches:
                    if match.start() > start_pos and match.start() < end_pos:
                        end_pos = match.start()
        
        # Extract the section content
        section_content = text[start_pos:end_pos].strip()
        
        # Remove the section header
        for header in section_headers:
            pattern = rf'(?i)\b{re.escape(header)}\b'
            section_content = re.sub(pattern, "", section_content, count=1).strip()
        
        return section_content