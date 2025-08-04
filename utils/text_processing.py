import re
import unicodedata
from typing import List, Optional

def clean_text(text: str) -> str:
    """
    Clean and normalize text.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return ""
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters that might cause issues
    text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}\'\"\@\/\#\$\%\^\&\*\+\=\~\`\<\>]', '', text)
    
    # Remove bullet points and replace with standard format
    text = re.sub(r'[\u2022\u2023\u25E6\u2043\u2219]', '•', text)
    
    # Normalize quotes
    text = re.sub(r'[\u2018\u2019]', "'", text)
    text = re.sub(r'[\u201C\u201D]', '"', text)
    
    # Normalize dashes
    text = re.sub(r'[\u2013\u2014]', '-', text)
    
    # Remove empty lines
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = '\n'.join(lines)
    
    return text

def extract_email(text: str) -> Optional[str]:
    """
    Extract email address from text.
    
    Args:
        text (str): Text to search
        
    Returns:
        Optional[str]: Extracted email or None if not found
    """
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, text)
    
    if match:
        return match.group(0)
    return None

def extract_phone(text: str) -> Optional[str]:
    """
    Extract phone number from text.
    
    Args:
        text (str): Text to search
        
    Returns:
        Optional[str]: Extracted phone number or None if not found
    """
    phone_pattern = r'(\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}[- ]?\d{4}'
    match = re.search(phone_pattern, text)
    
    if match:
        return match.group(0)
    return None

def extract_links(text: str) -> List[str]:
    """
    Extract URLs from text.
    
    Args:
        text (str): Text to search
        
    Returns:
        List[str]: List of extracted URLs
    """
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w\.-]*\??[/\w\.-=&%]*'
    matches = re.findall(url_pattern, text)
    
    return matches

def extract_dates(text: str) -> List[str]:
    """
    Extract dates from text.
    
    Args:
        text (str): Text to search
        
    Returns:
        List[str]: List of extracted dates
    """
    date_patterns = [
        r'\d{1,2}/\d{1,2}/\d{2,4}',
        r'\d{2,4}/\d{1,2}/\d{1,2}',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b',
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b'
    ]
    
    dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        dates.extend(matches)
    
    return dates

def normalize_skill_name(skill: str) -> str:
    """
    Normalize a skill name for consistent matching.
    
    Args:
        skill (str): Skill name to normalize
        
    Returns:
        str: Normalized skill name
    """
    # Convert to lowercase
    skill = skill.lower()
    
    # Remove common suffixes
    skill = re.sub(r'\s+(programming|language|development|software|framework|library)$', '', skill)
    
    # Replace common abbreviations
    abbreviations = {
        'js': 'javascript',
        'ts': 'typescript',
        'py': 'python',
        'rb': 'ruby',
        'cs': 'c#',
        'cpp': 'c++',
        'db': 'database',
        'ui': 'user interface',
        'ux': 'user experience',
        'ml': 'machine learning',
        'ai': 'artificial intelligence',
        'nlp': 'natural language processing',
        'cv': 'computer vision'
    }
    
    if skill in abbreviations:
        skill = abbreviations[skill]
    
    # Remove special characters
    skill = re.sub(r'[^\w\s]', '', skill)
    
    # Remove extra whitespace
    skill = re.sub(r'\s+', ' ', skill).strip()
    
    return skill