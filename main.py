import streamlit as st
import os
import tempfile
from pathlib import Path

# Import agents
from agents.resume_processor import ResumeProcessor
from agents.ats_scorer import ATSScorer
from agents.jd_analyzer import JDAnalyzer
from agents.recommendation_engine import RecommendationEngine
from agents.visualization_agent import VisualizationAgent

# Import database operations
from database.operations import DatabaseOperations

# Import utils
from utils.file_parsers import parse_file
from utils.enhanced_display import display_resume_data, display_jd_data
from utils.visualization_utils import display_score_breakdown, display_recommendations

# Import config
from config import APP_TITLE, APP_LAYOUT, MAX_FILE_SIZE, ALLOWED_EXTENSIONS

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Set page configuration
st.set_page_config(
    page_title=APP_TITLE,
    layout=APP_LAYOUT,
    initial_sidebar_state="expanded"
)

# Apply custom CSS
local_css("static/css/style.css")

# Initialize database connection
db_ops = DatabaseOperations()

# Initialize agents
resume_processor = ResumeProcessor()
ats_scorer = ATSScorer()
jd_analyzer = JDAnalyzer()
recommendation_engine = RecommendationEngine()
visualization_agent = VisualizationAgent()

def main():
    st.title(APP_TITLE)
    st.markdown("Upload your resume and a job description to get an ATS score and improvement suggestions.")
    
    # Create session state variables
    if 'resume_data' not in st.session_state:
        st.session_state.resume_data = None
    if 'jd_data' not in st.session_state:
        st.session_state.jd_data = None
    if 'score_data' not in st.session_state:
        st.session_state.score_data = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    
    # Create two columns for file uploads
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Upload Resume")
        resume_file = st.file_uploader(
            "Upload your resume (PDF, DOCX, TXT)",
            type=ALLOWED_EXTENSIONS,
            key="resume_uploader"
        )
        
        if resume_file is not None:
            # Check file size
            if resume_file.size > MAX_FILE_SIZE:
                st.error(f"File size exceeds the limit of {MAX_FILE_SIZE/1024/1024}MB")
                return
            
            # Process the resume file
            with st.spinner("Processing resume..."):
                # Save the uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{resume_file.name.split('.')[-1]}") as tmp:
                    tmp.write(resume_file.getvalue())
                    tmp_path = tmp.name
                
                try:
                    # Parse the file
                    resume_text = parse_file(tmp_path)
                    
                    # Process the resume
                    resume_data = resume_processor.process(resume_text)
                    st.session_state.resume_data = resume_data
                    
                    # Display a success message
                    st.success("Resume processed successfully!")
                    
                    # Display the enhanced resume data
                    with st.expander("View Extracted Resume Data", expanded=True):
                        display_resume_data(resume_data)
                
                except Exception as e:
                    st.error(f"Error processing resume: {str(e)}")
                
                finally:
                    # Clean up the temporary file
                    os.unlink(tmp_path)
    
    with col2:
        st.subheader("Upload Job Description")
        jd_file = st.file_uploader(
            "Upload job description (PDF, DOCX, TXT)",
            type=ALLOWED_EXTENSIONS,
            key="jd_uploader"
        )
        
        if jd_file is not None:
            # Check file size
            if jd_file.size > MAX_FILE_SIZE:
                st.error(f"File size exceeds the limit of {MAX_FILE_SIZE/1024/1024}MB")
                return
            
            # Process the job description file
            with st.spinner("Processing job description..."):
                # Save the uploaded file temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{jd_file.name.split('.')[-1]}") as tmp:
                    tmp.write(jd_file.getvalue())
                    tmp_path = tmp.name
                
                try:
                    # Parse the file
                    jd_text = parse_file(tmp_path)
                    
                    # Analyze the job description
                    jd_data = jd_analyzer.analyze(jd_text)
                    st.session_state.jd_data = jd_data
                    
                    # Display a success message
                    st.success("Job description processed successfully!")
                    
                    # Display the enhanced job description data
                    with st.expander("View Extracted Job Description Data", expanded=True):
                        display_jd_data(jd_data)
                
                except Exception as e:
                    st.error(f"Error processing job description: {str(e)}")
                
                finally:
                    # Clean up the temporary file
                    os.unlink(tmp_path)
    
    # Add a text area for manual job description entry
    with st.expander("Or enter job description manually"):
        jd_text = st.text_area("Paste the job description here", height=200)
        if st.button("Process Manual Job Description") and jd_text:
            with st.spinner("Processing job description..."):
                try:
                    # Analyze the job description
                    jd_data = jd_analyzer.analyze(jd_text)
                    st.session_state.jd_data = jd_data
                    
                    # Display a success message
                    st.success("Job description processed successfully!")
                    
                    # Display the enhanced job description data
                    with st.expander("View Extracted Job Description Data", expanded=True):
                        display_jd_data(jd_data)
                
                except Exception as e:
                    st.error(f"Error processing job description: {str(e)}")
    
    # Score the resume if both resume and job description are available
    if st.session_state.resume_data and st.session_state.jd_data:
        if st.button("Score Resume", type="primary"):
            with st.spinner("Scoring resume..."):
                try:
                    # Score the resume
                    score_data = ats_scorer.score(
                        resume_data=st.session_state.resume_data,
                        jd_data=st.session_state.jd_data
                    )
                    st.session_state.score_data = score_data
                    
                    # Generate recommendations
                    recommendations = recommendation_engine.generate_recommendations(
                        resume_data=st.session_state.resume_data,
                        jd_data=st.session_state.jd_data,
                        score_data=score_data
                    )
                    st.session_state.recommendations = recommendations
                    
                    # Save to database
                    db_ops.save_scoring_result(
                        resume_data=st.session_state.resume_data,
                        jd_data=st.session_state.jd_data,
                        score_data=score_data,
                        recommendations=recommendations
                    )
                    
                    # Display a success message
                    st.success("Resume scored successfully!")
                
                except Exception as e:
                    st.error(f"Error scoring resume: {str(e)}")
    
    # Display the score and recommendations if available
    if st.session_state.score_data:
        st.header("Resume Score")
        
        # Display the overall score
        overall_score = st.session_state.score_data.get("overall_score", 0)
        st.metric("Overall ATS Score", f"{overall_score:.1f}/100")
        
        # Display score breakdown
        display_score_breakdown(st.session_state.score_data)
        
        # Generate visualizations
        visualization_agent.generate_score_visualization(st.session_state.score_data)
    
    if st.session_state.recommendations:
        st.header("Improvement Recommendations")
        display_recommendations(st.session_state.recommendations)
        
        # Generate recommendation visualizations
        visualization_agent.generate_recommendation_visualization(
            st.session_state.recommendations,
            st.session_state.resume_data,
            st.session_state.jd_data
        )
    
    # Add download button for report
    if st.session_state.score_data and st.session_state.recommendations:
        if st.button("Download Report (PDF)"):
            # Generate PDF report
            report_path = visualization_agent.generate_pdf_report(
                resume_data=st.session_state.resume_data,
                jd_data=st.session_state.jd_data,
                score_data=st.session_state.score_data,
                recommendations=st.session_state.recommendations
            )
            
            # Provide download link
            with open(report_path, "rb") as file:
                st.download_button(
                    label="Download PDF Report",
                    data=file.read(),
                    file_name="ats_resume_report.pdf",
                    mime="application/pdf"
                )
            
            # Clean up the temporary file
            os.unlink(report_path)
    
    # Add a sidebar with additional options
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This ATS Resume Scoring System analyzes your resume against job descriptions to:
        
        - Extract and match skills
        - Evaluate experience relevance
        - Check education requirements
        - Score resume format
        - Provide improvement suggestions
        """)
        
        st.header("Tips")
        st.markdown("""
        - Use standard resume formats
        - Include keywords from job descriptions
        - Quantify your achievements
        - Keep it concise (1-2 pages)
        - Check for typos and grammar
        """)
        
        # Add a reset button
        if st.button("Reset All Data"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

if __name__ == "__main__":
    main()