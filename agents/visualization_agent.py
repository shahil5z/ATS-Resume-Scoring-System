import os
import tempfile
import io
import base64
from typing import Dict, List, Any, Optional
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from jinja2 import Environment, FileSystemLoader, Template

class VisualizationAgent:
    """
    Agent responsible for generating visualizations and reports.
    """
    
    def __init__(self):
        # Initialize visualization settings
        self.color_palette = px.colors.qualitative.Plotly
        self.styles = getSampleStyleSheet()
        
        # Create custom styles
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor('#2E86AB')
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.HexColor('#2E86AB')
        ))
    
    def generate_score_visualization(self, score_data: Dict[str, Any]) -> None:
        """
        Generate and display score visualizations.
        
        Args:
            score_data (Dict[str, Any]): Scoring results
        """
        # Create score breakdown chart
        breakdown = score_data.get("score_breakdown", {})
        
        # Prepare data for visualization
        categories = list(breakdown.keys())
        scores = [details.get("score", 0) for details in breakdown.values()]
        weights = [details.get("weight", 0) for details in breakdown.values()]
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Score by Category', 'Category Weights'),
            specs=[[{"type": "bar"}, {"type": "pie"}]]
        )
        
        # Add bar chart
        fig.add_trace(
            go.Bar(
                x=categories,
                y=scores,
                marker_color=self.color_palette[0],
                text=[f"{score:.1f}" for score in scores],
                textposition='auto',
            ),
            row=1, col=1
        )
        
        # Add pie chart
        fig.add_trace(
            go.Pie(
                labels=categories,
                values=weights,
                marker_colors=self.color_palette[:len(categories)],
                textinfo='label+percent',
                textposition='auto',
            ),
            row=1, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text="Resume Score Analysis",
            title_x=0.5,
            showlegend=False,
            height=400
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Display benchmark comparison
        benchmark = score_data.get("benchmark", {})
        if benchmark:
            self._display_benchmark_comparison(benchmark)
        
        # Display confidence interval
        confidence = score_data.get("confidence_interval", {})
        if confidence:
            self._display_confidence_interval(confidence, score_data.get("overall_score", 0))
    
    def _display_benchmark_comparison(self, benchmark: Dict[str, Any]) -> None:
        """Display benchmark comparison visualization."""
        # Create benchmark comparison chart
        fig = go.Figure()
        
        # Add average line
        fig.add_shape(
            type="line",
            x0=0, y0=benchmark.get("average", 0),
            x1=1, y1=benchmark.get("average", 0),
            line=dict(color="orange", width=2, dash="dash"),
        )
        
        # Add top performer line
        fig.add_shape(
            type="line",
            x0=0, y0=benchmark.get("top", 0),
            x1=1, y1=benchmark.get("top", 0),
            line=dict(color="green", width=2, dash="dash"),
        )
        
        # Add user score
        fig.add_trace(
            go.Scatter(
                x=[0.5],
                y=[benchmark.get("score", 0)],
                mode="markers",
                marker=dict(size=20, color=self.color_palette[0]),
                name=f"Your Score: {benchmark.get('score', 0):.1f}",
            )
        )
        
        # Update layout
        fig.update_layout(
            title=f"Industry Benchmark: {benchmark.get('industry', '').title()}",
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(title="Score"),
            annotations=[
                dict(
                    x=0.05,
                    y=benchmark.get("average", 0),
                    xref="x",
                    yref="y",
                    text=f"Average: {benchmark.get('average', 0):.1f}",
                    showarrow=False,
                    font=dict(color="orange")
                ),
                dict(
                    x=0.05,
                    y=benchmark.get("top", 0),
                    xref="x",
                    yref="y",
                    text=f"Top: {benchmark.get('top', 0):.1f}",
                    showarrow=False,
                    font=dict(color="green")
                ),
                dict(
                    x=0.5,
                    y=benchmark.get("score", 0),
                    xref="x",
                    yref="y",
                    text=f"Percentile: {benchmark.get('percentile', 0):.1f}%",
                    showarrow=True,
                    arrowhead=2,
                    ax=0,
                    ay=-30
                )
            ],
            height=300
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
    
    def _display_confidence_interval(self, confidence: Dict[str, Any], score: float) -> None:
        """Display confidence interval visualization."""
        # Create confidence interval chart
        fig = go.Figure()
        
        # Add confidence interval band
        fig.add_trace(
            go.Scatter(
                x=["Score"],
                y=[confidence.get("upper", 0)],
                mode="markers",
                marker=dict(size=15, color="lightgray", opacity=0.5),
                name="Upper Bound"
            )
        )
        
        fig.add_trace(
            go.Scatter(
                x=["Score"],
                y=[confidence.get("lower", 0)],
                mode="markers",
                marker=dict(size=15, color="lightgray", opacity=0.5),
                name="Lower Bound"
            )
        )
        
        # Add actual score
        fig.add_trace(
            go.Scatter(
                x=["Score"],
                y=[score],
                mode="markers",
                marker=dict(size=20, color=self.color_palette[0]),
                name=f"Score: {score:.1f}"
            )
        )
        
        # Add error bar
        fig.add_trace(
            go.Scatter(
                x=["Score"],
                y=[score],
                mode="markers",
                error_y=dict(
                    type="data",
                    symmetric=False,
                    arrayminus=[score - confidence.get("lower", 0)],
                    array=[confidence.get("upper", 0) - score],
                    color="gray",
                    thickness=2
                ),
                marker=dict(size=0),
                showlegend=False
            )
        )
        
        # Update layout
        fig.update_layout(
            title="Score Confidence Interval (95%)",
            yaxis=dict(title="Score"),
            height=300
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
    
    def generate_recommendation_visualization(self, recommendations: List[Dict[str, Any]], 
                                           resume_data: Dict[str, Any], 
                                           jd_data: Dict[str, Any]) -> None:
        """
        Generate and display recommendation visualizations.
        
        Args:
            recommendations (List[Dict[str, Any]]): List of recommendations
            resume_data (Dict[str, Any]): Structured resume data
            jd_data (Dict[str, Any]): Structured job description data
        """
        if not recommendations:
            return
        
        # Create recommendation priority chart
        df = pd.DataFrame(recommendations)
        
        # Create horizontal bar chart
        fig = px.bar(
            df,
            y="title",
            x="priority",
            orientation='h',
            color="category",
            color_discrete_sequence=self.color_palette,
            title="Recommendation Priority",
            labels={"priority": "Priority (Lower = Higher)", "title": "Recommendation"}
        )
        
        # Update layout
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            height=400
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Generate skills gap heatmap if applicable
        skills_gap_recs = [rec for rec in recommendations if rec.get("category") == "skills_gap"]
        if skills_gap_recs:
            self._generate_skills_gap_heatmap(resume_data, jd_data)
    
    def _generate_skills_gap_heatmap(self, resume_data: Dict[str, Any], jd_data: Dict[str, Any]) -> None:
        """Generate skills gap heatmap visualization."""
        # Get skills from resume and job description
        resume_skills = [skill.lower() for skill in resume_data.get("skills", [])]
        jd_required_skills = [skill.lower() for skill in jd_data.get("required_skills", [])]
        jd_preferred_skills = [skill.lower() for skill in jd_data.get("preferred_skills", [])]
        
        # Create a matrix of skills
        all_skills = list(set(resume_skills + jd_required_skills + jd_preferred_skills))
        
        # Create presence matrix
        presence_matrix = []
        for skill in all_skills:
            row = [
                1 if skill in resume_skills else 0,
                1 if skill in jd_required_skills else 0,
                1 if skill in jd_preferred_skills else 0
            ]
            presence_matrix.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(
            presence_matrix,
            index=all_skills,
            columns=["Resume", "JD Required", "JD Preferred"]
        )
        
        # Create heatmap
        fig = px.imshow(
            df,
            labels=dict(x="Source", y="Skill", color="Presence"),
            color_continuous_scale="Blues",
            title="Skills Gap Analysis"
        )
        
        # Update layout
        fig.update_layout(height=500)
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
    
    def generate_pdf_report(self, resume_data: Dict[str, Any], 
                           jd_data: Dict[str, Any], 
                           score_data: Dict[str, Any], 
                           recommendations: List[Dict[str, Any]]) -> str:
        """
        Generate a PDF report of the resume analysis.
        
        Args:
            resume_data (Dict[str, Any]): Structured resume data
            jd_data (Dict[str, Any]): Structured job description data
            score_data (Dict[str, Any]): Scoring results
            recommendations (List[Dict[str, Any]]): List of recommendations
            
        Returns:
            str: Path to the generated PDF file
        """
        # Create temporary file
        temp_path = os.path.join(tempfile.gettempdir(), "ats_resume_report.pdf")
        
        # Create PDF document
        doc = SimpleDocTemplate(temp_path, pagesize=letter)
        story = []
        
        # Add title
        title = Paragraph("ATS Resume Analysis Report", self.styles['CustomTitle'])
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Add job information
        job_title = jd_data.get("job_title", "Unknown Position")
        company = jd_data.get("company", "Unknown Company")
        job_info = Paragraph(f"<b>Job:</b> {job_title} at {company}", self.styles['Normal'])
        story.append(job_info)
        story.append(Spacer(1, 12))
        
        # Add overall score
        overall_score = score_data.get("overall_score", 0)
        score_text = f"<b>Overall ATS Score:</b> {overall_score:.1f}/100"
        score_para = Paragraph(score_text, self.styles['Normal'])
        story.append(score_para)
        story.append(Spacer(1, 12))
        
        # Add score breakdown
        story.append(Paragraph("Score Breakdown", self.styles['CustomHeading']))
        breakdown = score_data.get("score_breakdown", {})
        
        # Create table for score breakdown
        table_data = [["Category", "Score", "Weight"]]
        for category, details in breakdown.items():
            score = details.get("score", 0)
            weight = details.get("weight", 0)
            table_data.append([
                category.title(),
                f"{score:.1f}",
                f"{weight:.1%}"
            ])
        
        score_table = Table(table_data)
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(score_table)
        story.append(Spacer(1, 12))
        
        # Add benchmark information
        benchmark = score_data.get("benchmark", {})
        if benchmark:
            story.append(Paragraph("Industry Benchmark", self.styles['CustomHeading']))
            industry = benchmark.get("industry", "Unknown")
            percentile = benchmark.get("percentile", 0)
            benchmark_text = f"""
            <b>Industry:</b> {industry.title()}<br/>
            <b>Your Percentile:</b> {percentile:.1f}%<br/>
            <b>Industry Average:</b> {benchmark.get('average', 0):.1f}<br/>
            <b>Top Performer:</b> {benchmark.get('top', 0):.1f}
            """
            benchmark_para = Paragraph(benchmark_text, self.styles['Normal'])
            story.append(benchmark_para)
            story.append(Spacer(1, 12))
        
        # Add recommendations
        if recommendations:
            story.append(Paragraph("Improvement Recommendations", self.styles['CustomHeading']))
            
            for rec in recommendations:
                # Add recommendation title
                title = Paragraph(f"<b>{rec.get('title', '')}</b>", self.styles['Normal'])
                story.append(title)
                
                # Add recommendation description
                description = Paragraph(rec.get('description', ''), self.styles['Normal'])
                story.append(description)
                
                # Add suggestions
                suggestions = rec.get('suggestions', [])
                for suggestion in suggestions:
                    suggestion_para = Paragraph(f"• {suggestion}", self.styles['Normal'])
                    story.append(suggestion_para)
                
                story.append(Spacer(1, 12))
        
        # Build PDF
        doc.build(story)
        
        return temp_path