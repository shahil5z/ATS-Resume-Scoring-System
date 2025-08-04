import re
import json
from typing import Dict, List, Any, Optional
import spacy
from utils.text_processing import clean_text, extract_email, extract_phone, extract_links

class ResumeProcessor:
    """
    Agent responsible for processing resumes and extracting relevant information.
    """
    
    def __init__(self):
        # Load spaCy model for NLP tasks
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            # Fallback to a smaller model if the main one isn't available
            self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
        
        # Define regex patterns for common resume sections
        self.section_patterns = {
            "skills": r"(?i)(skills|technical skills|core competencies|expertise|proficiencies|technologies|tools|languages|certifications)",
            "experience": r"(?i)(work experience|professional experience|employment history|work history|career|experience|work)",
            "education": r"(?i)(education|academic background|qualifications|academic qualifications|education background|academic)",
            "summary": r"(?i)(summary|professional summary|career summary|about me|profile|objective|personal statement)",
            "contact": r"(?i)(contact|contact information|contact details|personal details|personal information)"
        }
        
        # Define patterns for extracting specific information
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}'
        self.date_pattern = r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{2,4}[/-]\d{1,2}[/-]\d{1,2}|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b)'
        
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
        
        # Institution patterns
        self.institution_patterns = [
            r'(University|College|Institute|School|Academy)',
            r'(Ltd|Inc|LLC|Corp|Corporation)',
            r'(of|at|in|and)'
        ]
        
        # Degree patterns
        self.degree_patterns = [
            r'(Bachelor|Master|PhD|Doctorate|Associate|B\.S\.|M\.S\.|B\.A\.|M\.A\.|B\.Eng|M\.Eng|B\.Tech|M\.Tech)',
            r'(Degree|Diploma|Certificate|Certification)',
            r'(BSc|MSc|BA|MA|BEng|MEng|BTech|MTech)'
        ]
        
        # Job title patterns
        self.job_title_patterns = [
            r'(Software Engineer|Developer|Programmer)',
            r'(Data Scientist|Analyst|Engineer)',
            r'(Project Manager|Product Manager)',
            r'(Designer|Architect)',
            r'(Consultant|Specialist|Expert)',
            r'(Director|Manager|Lead|Head|Chief)',
            r'(Intern|Trainee|Junior|Senior|Principal)'
        ]
    
    def process(self, resume_text: str) -> Dict[str, Any]:
        """
        Process the resume text and extract relevant information.
        
        Args:
            resume_text (str): Raw text extracted from the resume file
            
        Returns:
            Dict[str, Any]: Structured resume data in JSON format
        """
        # Clean the text
        cleaned_text = clean_text(resume_text)
        
        # Extract sections
        sections = self._extract_sections(cleaned_text)
        
        # Extract contact information
        contact_info = self._extract_contact_info(cleaned_text)
        
        # Extract skills from multiple sources
        skills_sections = [
            sections.get("skills", ""),
            sections.get("experience", ""),
            sections.get("summary", "")
        ]
        skills_text = " ".join(skills_sections)
        skills = self._extract_skills(skills_text)
        
        # Extract experience
        experience = self._extract_experience(sections.get("experience", ""))
        
        # Extract education
        education = self._extract_education(sections.get("education", ""))
        
        # Extract summary
        summary = self._extract_summary(sections.get("summary", ""))
        
        # If no summary found, try to extract from the beginning of the resume
        if not summary:
            summary = self._extract_summary_from_beginning(cleaned_text)
        
        # Construct the structured resume data
        resume_data = {
            "contact_info": contact_info,
            "skills": skills,
            "experience": experience,
            "education": education,
            "summary": summary,
            "raw_text": cleaned_text,
            "sections": sections
        }
        
        return resume_data
    
    def _extract_sections(self, text: str) -> Dict[str, str]:
        """
        Extract different sections from the resume text.
        
        Args:
            text (str): Cleaned resume text
            
        Returns:
            Dict[str, str]: Dictionary of section names and their content
        """
        sections = {}
        
        # Find section headers with their positions
        section_positions = {}
        for section_name, pattern in self.section_patterns.items():
            matches = list(re.finditer(pattern, text))
            if matches:
                # Store the position of the first match
                section_positions[section_name] = matches[0].start()
        
        # Sort sections by their position in the text
        sorted_sections = sorted(section_positions.items(), key=lambda x: x[1])
        
        # Extract section content
        for i, (section_name, start_pos) in enumerate(sorted_sections):
            # Determine the end position of the section
            if i < len(sorted_sections) - 1:
                end_pos = sorted_sections[i + 1][1]
            else:
                end_pos = len(text)
            
            # Extract the section content
            section_content = text[start_pos:end_pos].strip()
            
            # Remove the section header from the content
            header_pattern = self.section_patterns[section_name]
            section_content = re.sub(header_pattern, "", section_content, flags=re.IGNORECASE).strip()
            
            # Store the section content
            sections[section_name] = section_content
        
        return sections
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """
        Extract contact information from the resume text.
        
        Args:
            text (str): Cleaned resume text
            
        Returns:
            Dict[str, str]: Dictionary containing contact information
        """
        contact_info = {
            "email": extract_email(text),
            "phone": extract_phone(text),
            "links": extract_links(text),
            "name": self._extract_name(text),
            "location": self._extract_location(text)
        }
        
        return contact_info
    
    def _extract_name(self, text: str) -> Optional[str]:
        """
        Extract the candidate's name from the resume text.
        
        Args:
            text (str): Cleaned resume text
            
        Returns:
            Optional[str]: Extracted name or None if not found
        """
        # The name is typically at the beginning of the resume
        first_lines = text.split('\n')[:5]
        
        # Process each line with spaCy to find proper nouns
        for line in first_lines:
            doc = self.nlp(line)
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    return ent.text
        
        # Fallback: Look for capitalized words at the beginning
        first_line = text.split('\n')[0]
        words = first_line.split()
        
        # Look for 2-3 consecutive capitalized words (likely a name)
        for i in range(len(words) - 1):
            if words[i][0].isupper() and words[i+1][0].isupper():
                name = f"{words[i]} {words[i+1]}"
                # Check if it's likely a name (not a job title or section header)
                if not any(pattern in name.lower() for pattern in ["resume", "cv", "curriculum", "vitae"]):
                    return name
        
        return None
    
    def _extract_location(self, text: str) -> Optional[str]:
        """
        Extract the candidate's location from the resume text.
        
        Args:
            text (str): Cleaned resume text
            
        Returns:
            Optional[str]: Extracted location or None if not found
        """
        # Process the text with spaCy to find GPE (Geopolitical Entity) entities
        doc = self.nlp(text)
        
        for ent in doc.ents:
            if ent.label_ == "GPE":
                return ent.text
        
        # Fallback: Look for location patterns
        location_patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z]{2})',  # City, State
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z][a-z]+)',  # City, Country
            r'([A-Z]{2},\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # State, City
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from the resume text.
        
        Args:
            text (str): Text from skills and experience sections
            
        Returns:
            List[str]: List of extracted skills
        """
        skills = []
        
        # Extract skills based on predefined keywords
        for skill in self.skill_keywords:
            if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
                skills.append(skill)
        
        # Extract skills using NLP
        doc = self.nlp(text)
        
        # Look for noun phrases that might indicate skills
        for chunk in doc.noun_chunks:
            chunk_text = chunk.text.strip()
            
            # Check if the chunk is a skill (heuristic: 2-4 words, starts with capital letter)
            if chunk_text and 2 <= len(chunk_text.split()) <= 4 and chunk_text[0].isupper():
                # Check if it's not already in the predefined skills
                if chunk_text not in skills:
                    skills.append(chunk_text)
        
        # Look for skill sections with bullet points
        bullet_patterns = [
            r'•\s*([^•\n]+)',
            r'-\s*([^\-\n]+)',
            r'\*\s*([^\\\n]+)',
            r'\d+\.\s*([^\n]+)'
        ]
        
        for pattern in bullet_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                # Clean the match
                skill = match.strip()
                if skill and skill not in skills:
                    skills.append(skill)
        
        # Remove duplicates and empty skills
        skills = list(set(skill for skill in skills if skill.strip()))
        
        return skills
    
    def _extract_experience(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract work experience from the resume text.
        
        Args:
            text (str): Text from the experience section
            
        Returns:
            List[Dict[str, Any]]: List of experience entries
        """
        experiences = []
        
        # Split the text into potential experience entries
        # This is a heuristic approach and might need refinement
        lines = text.split('\n')
        current_experience = {}
        experience_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this line looks like a job title
            if self._is_job_title(line):
                # If we have collected lines for a previous experience, process them
                if experience_lines:
                    current_experience["description"] = " ".join(experience_lines)
                    experiences.append(current_experience)
                
                # Start a new experience entry
                current_experience = {
                    "title": line,
                    "company": "",
                    "duration": "",
                    "description": ""
                }
                experience_lines = []
            else:
                experience_lines.append(line)
        
        # Process the last experience entry if exists
        if experience_lines:
            current_experience["description"] = " ".join(experience_lines)
            experiences.append(current_experience)
        
        # Extract details from each experience entry
        for exp in experiences:
            description = exp.get("description", "")
            
            # Extract company name
            company = self._extract_company(description)
            if company:
                exp["company"] = company
            
            # Extract duration
            duration = self._extract_duration(description)
            if duration:
                exp["duration"] = duration
        
        return experiences
    
    def _is_job_title(self, text: str) -> bool:
        """
        Check if a line of text looks like a job title.
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if it looks like a job title
        """
        # Check if it matches any job title pattern
        for pattern in self.job_title_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        # Check if it's a short, capitalized phrase (likely a title)
        words = text.split()
        if 1 <= len(words) <= 5 and all(word[0].isupper() for word in words if word):
            # Exclude common non-title words
            if not any(word.lower() in ["responsibilities", "duties", "achievements", "accomplishments"] for word in words):
                return True
        
        return False
    
    def _extract_company(self, text: str) -> Optional[str]:
        """
        Extract company name from experience description.
        
        Args:
            text (str): Experience description
            
        Returns:
            Optional[str]: Company name or None if not found
        """
        company_patterns = [
            r'at\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'with\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|Ltd|LLC|Corp|Corporation|Company))',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),'
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                company = match.group(1)
                # Clean up the company name
                company = re.sub(r'\s+(?:Inc|Ltd|LLC|Corp|Corporation|Company).*$', '', company)
                return company.strip()
        
        return None
    
    def _extract_duration(self, text: str) -> Optional[str]:
        """
        Extract duration from experience description.
        
        Args:
            text (str): Experience description
            
        Returns:
            Optional[str]: Duration or None if not found
        """
        # Look for date patterns
        date_matches = re.findall(self.date_pattern, text)
        
        if len(date_matches) >= 2:
            # If we found at least two dates, join them with a dash
            return f"{date_matches[0]} - {date_matches[1]}"
        elif len(date_matches) == 1:
            # If we found only one date, use it as is
            return date_matches[0]
        
        return None
    
    def _extract_education(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract education information from the resume text.
        
        Args:
            text (str): Text from the education section
            
        Returns:
            List[Dict[str, Any]]: List of education entries
        """
        education_entries = []
        
        # Split the text into potential education entries
        lines = text.split('\n')
        current_education = {}
        education_lines = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this line looks like an institution
            if self._is_institution(line):
                # If we have collected lines for a previous education entry, process them
                if education_lines:
                    current_education["description"] = " ".join(education_lines)
                    education_entries.append(current_education)
                
                # Start a new education entry
                current_education = {
                    "institution": line,
                    "degree": "",
                    "field": "",
                    "duration": "",
                    "description": ""
                }
                education_lines = []
            else:
                education_lines.append(line)
        
        # Process the last education entry if exists
        if education_lines:
            current_education["description"] = " ".join(education_lines)
            education_entries.append(current_education)
        
        # Extract details from each education entry
        for edu in education_entries:
            description = edu.get("description", "")
            
            # Extract degree
            degree = self._extract_degree(description)
            if degree:
                edu["degree"] = degree
            
            # Extract field of study
            field = self._extract_field_of_study(description)
            if field:
                edu["field"] = field
            
            # Extract duration
            duration = self._extract_duration(description)
            if duration:
                edu["duration"] = duration
        
        return education_entries
    
    def _is_institution(self, text: str) -> bool:
        """
        Check if a line of text looks like an institution name.
        
        Args:
            text (str): Text to check
            
        Returns:
            bool: True if it looks like an institution name
        """
        # Check if it matches any institution pattern
        for pattern in self.institution_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        # Check if it's a capitalized phrase (likely an institution)
        words = text.split()
        if 1 <= len(words) <= 6 and all(word[0].isupper() for word in words if word):
            return True
        
        return False
    
    def _extract_degree(self, text: str) -> Optional[str]:
        """
        Extract degree from education description.
        
        Args:
            text (str): Education description
            
        Returns:
            Optional[str]: Degree or None if not found
        """
        for pattern in self.degree_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_field_of_study(self, text: str) -> Optional[str]:
        """
        Extract field of study from education description.
        
        Args:
            text (str): Education description
            
        Returns:
            Optional[str]: Field of study or None if not found
        """
        field_patterns = [
            r'in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'of\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'majoring?\s+in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'specializ(?:ing|ation)\s+in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'focused\s+on\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'
        ]
        
        for pattern in field_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_summary(self, text: str) -> str:
        """
        Extract the professional summary from the resume text.
        
        Args:
            text (str): Text from the summary section
            
        Returns:
            str: Professional summary
        """
        # Clean and return the summary text
        summary = text.strip()
        
        # Remove common summary headers
        summary = re.sub(r'(?i)(summary|professional summary|career summary|about me|profile|objective|personal statement)\s*:?\s*', '', summary)
        
        return summary
    
    def _extract_summary_from_beginning(self, text: str) -> str:
        """
        Extract a summary from the beginning of the resume if no summary section exists.
        
        Args:
            text (str): Full resume text
            
        Returns:
            str: Extracted summary
        """
        # Get the first few lines of the resume
        lines = text.split('\n')
        summary_lines = []
        
        # Collect lines until we hit a section header
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if this line is a section header
            is_section_header = False
            for pattern in self.section_patterns.values():
                if re.search(pattern, line, re.IGNORECASE):
                    is_section_header = True
                    break
            
            if is_section_header:
                break
            
            # Add the line to the summary
            summary_lines.append(line)
            
            # Limit summary to 3-5 lines
            if len(summary_lines) >= 5:
                break
        
        return " ".join(summary_lines)