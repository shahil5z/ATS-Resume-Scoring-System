import streamlit as st
from typing import Dict, List, Any

def display_score_breakdown(score_data: Dict[str, Any]) -> None:
    """
    Display score breakdown in Streamlit.
    
    Args:
        score_data (Dict[str, Any]): Score breakdown data
    """
    breakdown = score_data.get("score_breakdown", {})
    
    # Create columns for each category
    cols = st.columns(len(breakdown))
    
    for i, (category, details) in enumerate(breakdown.items()):
        with cols[i]:
            score = details.get("score", 0)
            weight = details.get("weight", 0)
            
            # Display category score
            st.metric(
                label=f"{category.title()} ({weight:.0%})",
                value=f"{score:.1f}/100"
            )
            
            # Display details in expander
            with st.expander("Details"):
                details_data = details.get("details", {})
                
                if category == "skills":
                    st.write("**Required Skills Matched:**")
                    st.write(", ".join(details_data.get("required_matches", [])))
                    
                    st.write("**Required Skills Missing:**")
                    st.write(", ".join(details_data.get("required_gaps", [])))
                    
                    st.write("**Preferred Skills Matched:**")
                    st.write(", ".join(details_data.get("preferred_matches", [])))
                    
                    st.write("**Preferred Skills Missing:**")
                    st.write(", ".join(details_data.get("preferred_gaps", [])))
                
                elif category == "experience":
                    st.write(f"**Total Years of Experience:** {details_data.get('total_years', 0)}")
                    st.write(f"**Required Years:** {details_data.get('required_years', 0)}")
                    
                    st.write("**Relevant Experience:**")
                    for exp in details_data.get("relevant_experience", []):
                        st.write(f"- {exp}")
                
                elif category == "education":
                    level_met = "✅" if details_data.get("level_met", False) else "❌"
                    field_met = "✅" if details_data.get("field_met", False) else "❌"
                    
                    st.write(f"**Education Level Met:** {level_met}")
                    st.write(f"**Field of Study Met:** {field_met}")
                    
                    st.write(f"**Required Level:** {details_data.get('required_level', 'N/A')}")
                    st.write(f"**Required Fields:** {', '.join(details_data.get('required_fields', []))}")
                
                elif category == "format":
                    st.write("**Sections Present:**")
                    for section, present in details_data.get("sections", {}).items():
                        status = "✅" if present else "❌"
                        st.write(f"{status} {section.title()}")
                    
                    st.write("**Contact Info Present:**")
                    for field, present in details_data.get("contact", {}).items():
                        status = "✅" if present else "❌"
                        st.write(f"{status} {field.title()}")

def display_recommendations(recommendations: List[Dict[str, Any]]) -> None:
    """
    Display recommendations in Streamlit.
    
    Args:
        recommendations (List[Dict[str, Any]]): List of recommendations
    """
    for i, rec in enumerate(recommendations):
        # Create a container for each recommendation
        with st.container():
            # Display recommendation title with priority indicator
            priority = rec.get("priority", 0)
            priority_text = "High" if priority <= 2 else "Medium" if priority <= 4 else "Low"
            priority_color = "red" if priority <= 2 else "orange" if priority <= 4 else "green"
            
            st.markdown(f"### :{priority_color}[{rec.get('title', '')}] (Priority: {priority_text})")
            
            # Display description
            st.write(rec.get("description", ""))
            
            # Display suggestions
            suggestions = rec.get("suggestions", [])
            if suggestions:
                st.write("**Suggestions:**")
                for suggestion in suggestions:
                    st.write(f"- {suggestion}")
            
            # Add separator between recommendations
            if i < len(recommendations) - 1:
                st.divider()