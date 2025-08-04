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
-![image alt]()

**Job Description Analysis Agent**
**Overall Accuracy: 80-90%**
-![image alt]()

**ATS Scoring Agent**
**Overall Accuracy: 70-80%**
-![image alt]()

**Recommendation Engine**
**Overall Accuracy: 65-75%**
-![image alt]()

**Visualization Agent**
**Overall Accuracy: 90-95%**
-![image alt]()

**Overall System Accuracy**
**Combined Accuracy: 70-80%**

The system provides a reliable first-pass evaluation of resumes against job descriptions. While not perfect, it identifies major gaps and provides valuable feedback for improvement. The accuracy is highest for technical skills, education requirements, and format issues, and slightly lower for nuanced experience evaluation and context-specific recommendations.

---

## Setup

```bash
# Clone the repository
git clone https://github.com/shahil5z/ATS-Resume-Scoring-System.git
cd ATS-Resume-Scoring-System

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Create .env file and add your OpenAI API key
# Example:
# OPENAI_API_KEY=your_openai_api_key_here

# Run the application
python run.py

## Usage

### Start the Application:
  python run.py
The application will open in your web browser.

### Upload Your Resume:
- Click "Upload Resume" and select your resume file (PDF, DOCX, or TXT)
- Review the extracted data in the "View Extracted Resume Data" section


### Provide Job Description:
- Upload a job description file or paste the text directly
- Review the extracted requirements in the "View Extracted Job Description Data" section

### Score Your Resume:
- Click "Score Resume" to analyze your resume against the job description
- Review your overall ATS score and detailed breakdown

### Review Recommendations:
- Examine the improvement recommendations
- Focus on high-priority suggestions first

### Download Report:
- Click "Download Report (PDF)" to save a comprehensive analysis
- Use this report to track your improvements over time

## System Architecture
The ATS Resume Scoring System consists of several specialized agents working together:

### Core Components

***Resume Processing Agent***
- Extracts and structures data from resumes
- Identifies contact information, skills, experience, education, and summary
- Handles multiple file formats and structures

***Job Description Analysis Agent***
- Parses job descriptions to identify requirements
- Extracts required and preferred skills, experience needs, and education requirements
- Structures unstructured job description text

***ATS Scoring Agent***
- Evaluates resume-job description match across multiple dimensions
- Provides weighted scoring based on industry standards
- Calculates confidence intervals for scores

***Recommendation Engine***
- Generates specific, actionable improvement suggestions
- Prioritizes recommendations based on impact
- Provides context-aware advice

***Visualization Agent***
- Creates interactive charts and graphs
- Generates professional PDF reports
- Provides visual analysis of skills gaps and benchmarks

### Supporting Components

***Database Integration***
- Stores scoring results and history
- Supports both SQLite and MongoDB
Enables session management and result tracking

***RAG (Retrieval-Augmented Generation) System***
- Provides enhanced insights using industry benchmarks
- Offers context-specific recommendations
- Improves with continued use***

***File Processing Utilities***
- Handles multiple file formats (PDF, DOCX, TXT)
- Extracts text while preserving structure
- Cleans and normalizes text for analysis

### Technology Stack

***Frontend***: Streamlit for responsive web interface
***NLP***: spaCy for text processing and entity recognition
***File Parsing***: PyPDF2, pdfplumber, python-docx
***Visualization***: Plotly, Matplotlib, Seaborn
***Database***: SQLAlchemy (SQLite) or PyMongo (MongoDB)
***RAG***: ChromaDB or FAISS with LangChain
***AI Enhancement***: OpenAI API for advanced features

### Limitations
While the ATS Resume Scoring System is powerful, it has some limitations:

***Format Dependency***: Works best with standard resume formats; creative or non-traditional formats may not parse as accurately.
***Industry Specificity***: Provides general industry benchmarks but may not capture nuances of specialized fields.
***Context Understanding***: Cannot assess the quality or impact of achievements, only their presence.
***Cultural Fit***: Does not evaluate soft skills or cultural alignment with companies.
***Language Support***: Currently optimized for English resumes; other languages may have reduced accuracy.