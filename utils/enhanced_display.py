import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Optional
import re

def display_resume_data(resume_data: Dict[str, Any]):
    """
    Display resume data in an enhanced, visually appealing format.
    
    Args:
        resume_data (Dict[str, Any]): Structured resume data
    """
    if not resume_data:
        st.warning("No resume data available.")
        return
    
    # Create a header with the candidate's name
    contact_info = resume_data.get("contact_info", {})
    name = contact_info.get("name", "Candidate")
    
    st.markdown(f"### 📄 Resume Analysis: {name}")
    
    # Create a summary card at the top
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Skills Count", len(resume_data.get("skills", [])))
    
    with col2:
        st.metric("Experience Entries", len(resume_data.get("experience", [])))
    
    with col3:
        st.metric("Education Entries", len(resume_data.get("education", [])))
    
    with col4:
        summary_length = len(resume_data.get("summary", ""))
        st.metric("Summary Length", f"{summary_length} chars")
    
    st.markdown("---")
    
    # Contact Information Section
    with st.expander("📇 Contact Information", expanded=True):
        if contact_info:
            contact_df = pd.DataFrame([
                {"Field": "Name", "Value": contact_info.get("name", "N/A")},
                {"Field": "Email", "Value": contact_info.get("email", "N/A")},
                {"Field": "Phone", "Value": contact_info.get("phone", "N/A")},
                {"Field": "Location", "Value": contact_info.get("location", "N/A")}
            ])
            
            st.dataframe(contact_df, use_container_width=True, hide_index=True)
            
            # Display links if available
            links = contact_info.get("links", [])
            if links:
                st.markdown("**Links:**")
                for link in links:
                    st.markdown(f"- {link}")
        else:
            st.write("No contact information found.")
    
    # Summary Section
    summary = resume_data.get("summary", "")
    if summary:
        with st.expander("📝 Professional Summary", expanded=True):
            st.markdown(f"> {summary}")
    else:
        with st.expander("📝 Professional Summary", expanded=True):
            st.warning("No professional summary found in the resume.")
    
    # Skills Section
    skills = resume_data.get("skills", [])
    if skills:
        with st.expander("🛠️ Skills", expanded=True):
            # Group skills by category for better visualization
            skill_categories = categorize_skills(skills)
            
            for category, category_skills in skill_categories.items():
                st.markdown(f"**{category}**")
                
                # Create skill tags with better contrast
                skills_html = " ".join([
                    f'<span style="background-color:#1E88E5; color:white; padding: 0.2em 0.5em; border-radius: 0.5em; margin: 0.2em; display: inline-block; word-wrap: break-word;">{skill}</span>'
                    for skill in category_skills
                ])
                st.markdown(skills_html, unsafe_allow_html=True)
    else:
        with st.expander("🛠️ Skills", expanded=True):
            st.warning("No skills found in the resume.")
    
    # Experience Section
    experience = resume_data.get("experience", [])
    if experience:
        with st.expander("💼 Work Experience", expanded=True):
            for i, exp in enumerate(experience):
                st.markdown(f"**{exp.get('title', 'Unknown Position')}**")
                
                # Create a sub-expander for each experience entry
                with st.expander(f"Details for {exp.get('title', 'Position')}"):
                    exp_df = pd.DataFrame([
                        {"Field": "Company", "Value": exp.get("company", "N/A")},
                        {"Field": "Duration", "Value": exp.get("duration", "N/A")},
                        {"Field": "Description", "Value": exp.get("description", "N/A")}
                    ])
                    st.dataframe(exp_df, use_container_width=True, hide_index=True)
    else:
        with st.expander("💼 Work Experience", expanded=True):
            st.warning("No work experience found in the resume.")
    
    # Education Section
    education = resume_data.get("education", [])
    if education:
        with st.expander("🎓 Education", expanded=True):
            for i, edu in enumerate(education):
                st.markdown(f"**{edu.get('institution', 'Unknown Institution')}**")
                
                # Create a sub-expander for each education entry
                with st.expander(f"Details for {edu.get('institution', 'Institution')}"):
                    edu_df = pd.DataFrame([
                        {"Field": "Degree", "Value": edu.get("degree", "N/A")},
                        {"Field": "Field of Study", "Value": edu.get("field", "N/A")},
                        {"Field": "Duration", "Value": edu.get("duration", "N/A")}
                    ])
                    st.dataframe(edu_df, use_container_width=True, hide_index=True)
    else:
        with st.expander("🎓 Education", expanded=True):
            st.warning("No education information found in the resume.")

def display_jd_data(jd_data: Dict[str, Any]):
    """
    Display job description data in an enhanced, visually appealing format.
    
    Args:
        jd_data (Dict[str, Any]): Structured job description data
    """
    if not jd_data:
        st.warning("No job description data available.")
        return
    
    # Create a header with the job title and company
    job_title = jd_data.get("job_title", "Unknown Position")
    company = jd_data.get("company", "Unknown Company")
    industry = jd_data.get("industry", "Unknown Industry")
    
    st.markdown(f"### 📋 Job Description: {job_title} at {company}")
    st.caption(f"Industry: {industry.title()}")
    
    # Create a summary card at the top
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Required Skills", len(jd_data.get("required_skills", [])))
    
    with col2:
        st.metric("Preferred Skills", len(jd_data.get("preferred_skills", [])))
    
    with col3:
        exp_req = jd_data.get("experience_requirements", {})
        years = exp_req.get("years", 0)
        st.metric("Years Required", f"{years}+ years")
    
    st.markdown("---")
    
    # Job Overview
    with st.expander("📊 Job Overview", expanded=True):
        jd_df = pd.DataFrame([
            {"Field": "Job Title", "Value": job_title},
            {"Field": "Company", "Value": company},
            {"Field": "Industry", "Value": industry.title()}
        ])
        st.dataframe(jd_df, use_container_width=True, hide_index=True)
    
    # Experience Requirements
    experience_req = jd_data.get("experience_requirements", {})
    if experience_req:
        with st.expander("💼 Experience Requirements", expanded=True):
            exp_df = pd.DataFrame([
                {"Field": "Years of Experience", "Value": f"{experience_req.get('years', 0)}+ years"},
                {"Field": "Keywords", "Value": ", ".join(experience_req.get("keywords", []))}
            ])
            st.dataframe(exp_df, use_container_width=True, hide_index=True)
    else:
        with st.expander("💼 Experience Requirements", expanded=True):
            st.warning("No specific experience requirements found.")
    
    # Education Requirements
    education_req = jd_data.get("education_requirements", {})
    if education_req:
        with st.expander("🎓 Education Requirements", expanded=True):
            edu_df = pd.DataFrame([
                {"Field": "Required Level", "Value": education_req.get("level", "N/A")},
                {"Field": "Fields of Study", "Value": ", ".join(education_req.get("fields", []))}
            ])
            st.dataframe(edu_df, use_container_width=True, hide_index=True)
    else:
        with st.expander("🎓 Education Requirements", expanded=True):
            st.warning("No specific education requirements found.")
    
    # Skills Section
    required_skills = jd_data.get("required_skills", [])
    preferred_skills = jd_data.get("preferred_skills", [])
    
    if required_skills or preferred_skills:
        with st.expander("🛠️ Skills Requirements", expanded=True):
            if required_skills:
                st.markdown("**Required Skills:**")
                req_skills_html = " ".join([
                    f'<span style="background-color:#E53935; color:white; padding: 0.2em 0.5em; border-radius: 0.5em; margin: 0.2em; display: inline-block; word-wrap: break-word;">{skill}</span>'
                    for skill in required_skills
                ])
                st.markdown(req_skills_html, unsafe_allow_html=True)
            
            if preferred_skills:
                st.markdown("**Preferred Skills:**")
                pref_skills_html = " ".join([
                    f'<span style="background-color:#43A047; color:white; padding: 0.2em 0.5em; border-radius: 0.5em; margin: 0.2em; display: inline-block; word-wrap: break-word;">{skill}</span>'
                    for skill in preferred_skills
                ])
                st.markdown(pref_skills_html, unsafe_allow_html=True)
    else:
        with st.expander("🛠️ Skills Requirements", expanded=True):
            st.warning("No skills requirements found.")
    
    # Responsibilities Section
    responsibilities = jd_data.get("responsibilities", [])
    if responsibilities:
        with st.expander("📋 Responsibilities", expanded=True):
            for i, responsibility in enumerate(responsibilities):
                st.markdown(f"{i+1}. {responsibility}")
    else:
        with st.expander("📋 Responsibilities", expanded=True):
            st.warning("No responsibilities found.")
    
    # Qualifications Section
    qualifications = jd_data.get("qualifications", [])
    if qualifications:
        with st.expander("✅ Qualifications", expanded=True):
            for i, qualification in enumerate(qualifications):
                st.markdown(f"{i+1}. {qualification}")
    else:
        with st.expander("✅ Qualifications", expanded=True):
            st.warning("No qualifications found.")

def categorize_skills(skills: List[str]) -> Dict[str, List[str]]:
    """
    Categorize skills into different categories for better visualization.
    
    Args:
        skills (List[str]): List of skills
        
    Returns:
        Dict[str, List[str]]: Dictionary of skill categories
    """
    # Define skill categories with keywords
    categories = {
        "Programming Languages": [
            "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "Ruby", "PHP", "Swift", "Kotlin",
            "Go", "Rust", "Scala", "R", "MATLAB", "Perl", "Shell", "Bash", "PowerShell"
        ],
        "Web Development": [
            "HTML", "CSS", "React", "Angular", "Vue", "Node.js", "Express", "Django", "Flask",
            "ASP.NET", "Spring", "Ruby on Rails", "Laravel", "Symfony", "jQuery", "Bootstrap",
            "Next.js", "Nuxt.js", "Svelte", "Gatsby", "Ember.js", "Backbone.js"
        ],
        "Databases": [
            "SQL", "MySQL", "PostgreSQL", "MongoDB", "Oracle", "SQLite", "Redis", "Cassandra",
            "DynamoDB", "Firebase", "Elasticsearch", "GraphQL", "MariaDB", "CouchDB"
        ],
        "Data Science & AI": [
            "Machine Learning", "Deep Learning", "Data Science", "Data Analysis", "Statistics",
            "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy", "NLTK",
            "Computer Vision", "NLP", "Big Data", "Hadoop", "Spark", "Tableau", "Power BI",
            "Jupyter", "Kaggle", "Data Visualization", "Predictive Modeling", "Statistical Analysis"
        ],
        "DevOps & Cloud": [
            "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "Git",
            "CI/CD", "Terraform", "Ansible", "Linux", "Unix", "Networking", "Security",
            "Microservices", "Serverless", "DevOps", "Agile", "Scrum", "Kanban"
        ],
        "Project Management": [
            "Project Management", "PMP", "Agile", "Scrum", "Kanban", "Waterfall", "JIRA",
            "Trello", "Asana", "Risk Management", "Budgeting", "Planning", "Team Leadership"
        ],
        "Soft Skills": [
            "Leadership", "Communication", "Teamwork", "Problem Solving", "Critical Thinking",
            "Time Management", "Creativity", "Adaptability", "Collaboration", "Emotional Intelligence",
            "Public Speaking", "Negotiation", "Conflict Resolution", "Decision Making", "Interpersonal Skills"
        ]
    }
    
    # Initialize categorized skills
    categorized_skills = {category: [] for category in categories}
    categorized_skills["Other"] = []
    
    # Categorize each skill
    for skill in skills:
        skill = skill.strip()  # Remove any extra whitespace
        if not skill:  # Skip empty skills
            continue
            
        categorized = False
        
        for category, category_skills in categories.items():
            if skill in category_skills:
                categorized_skills[category].append(skill)
                categorized = True
                break
        
        if not categorized:
            categorized_skills["Other"].append(skill)
    
    # Remove empty categories
    return {category: skills_list for category, skills_list in categorized_skills.items() if skills_list}