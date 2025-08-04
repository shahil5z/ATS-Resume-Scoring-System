# ATS Resume Scoring System

A comprehensive web application that analyzes resumes against job descriptions to provide ATS scores, detailed feedback, and improvement recommendations.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Accuracy Breakdown](#accuracy-breakdown)
- [Installation](#installation)
- [Usage](#usage)
- [System Architecture](#system-architecture)
- [License](#license)

---

## Overview

The **ATS Resume Scoring System** helps job seekers optimize their resumes for Applicant Tracking Systems (ATS) used by recruiters. By uploading your resume and a job description, the system analyzes how well your resume matches the job requirements and provides actionable feedback to improve your chances of getting noticed.

---

## Features

### 1. Resume Processing
- **Multi-format Support**: Upload resumes in PDF, DOCX, or TXT format  
- **Intelligent Parsing**: Extracts contact information, skills, experience, education, and professional summary  
- **Visual Display**: Clean, organized presentation of extracted resume data  

### 2. Job Description Analysis
- **Flexible Input**: Upload job descriptions as files or paste text directly  
- **Requirement Extraction**: Identifies required and preferred skills, experience needs, and education requirements  
- **Structured Display**: Organized presentation of job requirements  

### 3. ATS Scoring System
- **Comprehensive Scoring**: Evaluates skills match, experience relevance, education alignment, and format quality  
- **Industry Benchmarks**: Compares your resume against industry-specific standards  
- **Confidence Intervals**: Provides statistical confidence in the scoring results  

### 4. Improvement Recommendations
- **Specific Feedback**: Targeted suggestions for improving your resume  
- **Priority-Based**: Recommendations ordered by importance  
- **Actionable Advice**: Clear, practical steps to enhance your resume  

### 5. Visual Analytics
- **Score Visualization**: Interactive charts showing score breakdowns  
- **Skills Gap Analysis**: Visual representation of missing skills  
- **Benchmark Comparison**: How your resume compares to industry standards  

### 6. Report Generation
- **PDF Reports**: Download comprehensive analysis reports  
- **Professional Format**: Clean, shareable documentation of your resume analysis  

---

## How It Works

1. **Upload Your Resume**: Upload your resume in PDF, DOCX, or TXT format  
2. **Provide Job Description**: Upload a job description file or paste the text directly  
3. **Analyze and Score**: Click "Score Resume" to analyze your resume against the job requirements  
4. **Review Results**: View your ATS score, detailed breakdown, and improvement recommendations  
5. **Download Report**: Generate and download a PDF report of the analysis  

---

## Accuracy Breakdown

Our system uses multiple AI agents to analyze resumes and job descriptions. Here's how accurate each component is:

**Resume Processing Agent**
**Overall Accuracy: 75-85%**
-![image alt](https://github.com/shahil5z/ATS-Resume-Scoring-System/blob/7c30b3bc2b275650651bf9aa9865b0d07ecb011a/Accuracy%20Breakdown/1%20-%20Resume%20Processing%20Agent.png)

**Job Description Analysis Agent**
**Overall Accuracy: 80-90%**
-![image alt](https://github.com/shahil5z/ATS-Resume-Scoring-System/blob/7c30b3bc2b275650651bf9aa9865b0d07ecb011a/Accuracy%20Breakdown/2%20-%20Job%20Description%20Analysis%20Agent.png)

**ATS Scoring Agent**
**Overall Accuracy: 70-80%**
-![image alt](https://github.com/shahil5z/ATS-Resume-Scoring-System/blob/7c30b3bc2b275650651bf9aa9865b0d07ecb011a/Accuracy%20Breakdown/3%20-%20ATS%20Scoring%20Agent.png)

**Recommendation Engine**
**Overall Accuracy: 65-75%**
-![image alt](https://github.com/shahil5z/ATS-Resume-Scoring-System/blob/7c30b3bc2b275650651bf9aa9865b0d07ecb011a/Accuracy%20Breakdown/4%20-%20Recommendation%20Engine.png)

**Visualization Agent**
**Overall Accuracy: 90-95%**
-![image alt](https://github.com/shahil5z/ATS-Resume-Scoring-System/blob/7c30b3bc2b275650651bf9aa9865b0d07ecb011a/Accuracy%20Breakdown/5%20-%20Visualization%20Agent.png)

**Overall System Accuracy**
**Combined Accuracy: 70-80%**

The system provides a reliable first-pass evaluation of resumes against job descriptions. While not perfect, it identifies major gaps and provides valuable feedback for improvement. The accuracy is highest for technical skills, education requirements, and format issues, and slightly lower for nuanced experience evaluation and context-specific recommendations.

---

## installation

```bash
# Clone the repository
git clone https://github.com/shahil5z/ATS-Resume-Scoring-System.git
cd ATS-Resume-Scoring-System
```

### Create virtual environment
```bash
python -m venv venv
```

### Activate virtual environment
***On Windows***
```bash
venv\Scripts\activate
```
***On macOS/Linux***
```bash
source venv/bin/activate
```

# Install dependencies
```bash
pip install -r requirements.txt
```

# Download spaCy model
```bash
python -m spacy download en_core_web_sm
```

# Create .env file and add your OpenAI API key
```bash
# OPENAI_API_KEY=your_openai_api_key_here
```

### ADD THESE IN .ENV UNDER YOUR OPENAI KEY
```bash
# Database Configuration
DB_TYPE=sqlite  # Options: "sqlite", "mongodb"

# For SQLite
SQLITE_DB_PATH=ats_resume.db

# For MongoDB
MONGO_URI=mongodb://localhost:27017/
MONGO_DB_NAME=ats_resume_db

# RAG Configuration
RAG_VECTOR_STORE=chroma  # Options: "chroma", "faiss"
RAG_EMBEDDING_MODEL=text-embedding-ada-002
```

# Run the application
```bash
python run.py
```

---

## Usage

### Start the Application:
  python run.py
The application will open in your web browser.

2. **Upload Your Resume**:
   - Click "Upload Resume" and select your resume file (PDF, DOCX, or TXT)
   - Review the extracted data in the "View Extracted Resume Data" section

3. **Provide Job Description**:
   - Upload a job description file or paste the text directly
   - Review the extracted requirements in the "View Extracted Job Description Data" section

4. **Score Your Resume**:
   - Click "Score Resume" to analyze your resume against the job description
   - Review your overall ATS score and detailed breakdown

5. **Review Recommendations**:
   - Examine the improvement recommendations
   - Focus on high-priority suggestions first

6. **Download Report**:
   - Click "Download Report (PDF)" to save a comprehensive analysis
   - Use this report to track your improvements over time

## System Architecture

The ATS Resume Scoring System consists of several specialized agents working together:

### Core Components

1. **Resume Processing Agent**
   - Extracts and structures data from resumes
   - Identifies contact information, skills, experience, education, and summary
   - Handles multiple file formats and structures

2. **Job Description Analysis Agent**
   - Parses job descriptions to identify requirements
   - Extracts required and preferred skills, experience needs, and education requirements
   - Structures unstructured job description text

3. **ATS Scoring Agent**
   - Evaluates resume-job description match across multiple dimensions
   - Provides weighted scoring based on industry standards
   - Calculates confidence intervals for scores

4. **Recommendation Engine**
   - Generates specific, actionable improvement suggestions
   - Prioritizes recommendations based on impact
   - Provides context-aware advice

5. **Visualization Agent**
   - Creates interactive charts and graphs
   - Generates professional PDF reports
   - Provides visual analysis of skills gaps and benchmarks

### Supporting Components

1. **Database Integration**
   - Stores scoring results and history
   - Supports both SQLite and MongoDB
   - Enables session management and result tracking

2. **RAG (Retrieval-Augmented Generation) System**
   - Provides enhanced insights using industry benchmarks
   - Offers context-specific recommendations
   - Improves with continued use

3. **File Processing Utilities**
   - Handles multiple file formats (PDF, DOCX, TXT)
   - Extracts text while preserving structure
   - Cleans and normalizes text for analysis

### Technology Stack

- **Frontend**: Streamlit for responsive web interface
- **NLP**: spaCy for text processing and entity recognition
- **File Parsing**: PyPDF2, pdfplumber, python-docx
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Database**: SQLAlchemy (SQLite) or PyMongo (MongoDB)
- **RAG**: ChromaDB or FAISS with LangChain
- **AI Enhancement**: OpenAI API for advanced features

## Limitations

While the ATS Resume Scoring System is powerful, it has some limitations:

1. **Format Dependency**: Works best with standard resume formats; creative or non-traditional formats may not parse as accurately.

2. **Industry Specificity**: Provides general industry benchmarks but may not capture nuances of specialized fields.

3. **Context Understanding**: Cannot assess the quality or impact of achievements, only their presence.

4. **Cultural Fit**: Does not evaluate soft skills or cultural alignment with companies.

5. **Language Support**: Currently optimized for English resumes; other languages may have reduced accuracy.

## Contributing

We welcome contributions to improve the ATS Resume Scoring System! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- The spaCy team for the excellent NLP library
- Streamlit for the intuitive web framework
- The open-source community for various parsing and visualization tools
