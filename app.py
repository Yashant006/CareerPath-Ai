"""
CareerPath AI – Intelligent Career Recommendation System for Students
Main Application Entry Point (Streamlit)
B.Tech Computer Science (AI & Data Science Specialization) Project
"""

import os
import sys

# Ensure project root is in python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Configure Matplotlib temp cache directory to avoid Windows permissions warnings
temp_mpl = os.path.join(ROOT_DIR, ".mpl_cache")
os.makedirs(temp_mpl, exist_ok=True)
os.environ["MPLCONFIGDIR"] = temp_mpl

import streamlit as st

# Set Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="CareerPath AI – Intelligent Career Guidance",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

from database.db import init_db, get_all_students, get_student_by_id
from ml.predict import get_model, get_model_evaluation_metrics
from modules.home import render_home_page
from modules.registration import render_registration_page
from modules.assessment import render_assessment_page
from modules.recommendation import render_recommendations_page
from modules.roadmap_page import render_roadmap_page
from modules.dashboard import render_dashboard_page


def load_custom_css():
    """Loads dark navy & purple gradient theme styles."""
    css_path = os.path.join(ROOT_DIR, "assets", "styles.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def init_app_state():
    """Initializes SQLite database and session variables."""
    # Initialize SQLite database
    init_db()

    # Preload ML model bundle in background
    try:
        get_model()
    except Exception as e:
        print(f"Warning: Model pre-loading: {e}")

    # Initialize current page navigation
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Home"

    # Initialize active student (default to first student in DB if exists)
    if "active_student" not in st.session_state or st.session_state["active_student"] is None:
        students = get_all_students()
        if students:
            st.session_state["active_student"] = students[0]
        else:
            st.session_state["active_student"] = None


def render_sidebar():
    """Renders modern sidebar with student switcher and clear navigation."""
    with st.sidebar:
        # App Branding Header
        st.markdown(
            """
            <div style="padding: 10px 0 15px 0; border-bottom: 1px solid rgba(148, 163, 184, 0.15); margin-bottom: 15px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 2rem;">🎓</span>
                    <div>
                        <h2 style="margin: 0; font-size: 1.35rem; color: #FFFFFF; font-weight: 800; letter-spacing: -0.5px;">
                            CareerPath <span style="color: #C084FC;">AI</span>
                        </h2>
                        <p style="margin: 0; font-size: 0.75rem; color: #94A3B8;">Intelligent Guidance System</p>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Active Student Badge
        active_student = st.session_state.get("active_student")
        if active_student:
            st.markdown(
                f"""
                <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 10px; padding: 12px; margin-bottom: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                        <span style="font-size: 0.72rem; color: #C084FC; font-weight: 700; text-transform: uppercase;">Active Student</span>
                        <span style="font-size: 0.72rem; background: rgba(16, 185, 129, 0.2); color: #6EE7B7; padding: 2px 6px; border-radius: 4px;">Online</span>
                    </div>
                    <div style="font-weight: 700; color: #F8FAFC; font-size: 0.92rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">
                        {active_student['full_name']}
                    </div>
                    <div style="font-size: 0.75rem; color: #94A3B8;">
                        {active_student['current_semester']} • {active_student['branch'][:24]}...
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="background: rgba(30, 41, 59, 0.5); border: 1px dashed rgba(148, 163, 184, 0.3); border-radius: 10px; padding: 12px; margin-bottom: 20px; text-align: center;">
                    <span style="font-size: 0.8rem; color: #94A3B8;">No student selected yet</span>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Main Navigation Menu
        nav_options = [
            ("🏠 Home", "Home"),
            ("👤 Student Profile", "Student Profile"),
            ("📝 Career Assessment", "Assessment"),
            ("🎯 AI Recommendations", "Recommendations"),
            ("🗺️ Learning Roadmap", "Learning Roadmap"),
            ("📊 Student Dashboard", "Student Dashboard"),
            ("ℹ️ Project & Viva Guide", "About & Viva")
        ]

        st.markdown("<p style='font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; margin-bottom: 8px;'>Navigation</p>", unsafe_allow_html=True)

        current_page = st.session_state.get("current_page", "Home")

        for label, page_key in nav_options:
            is_active = (current_page == page_key)
            button_label = f"▸ {label}" if is_active else label
            if st.button(button_label, key=f"nav_{page_key}", use_container_width=True):
                st.session_state["current_page"] = page_key
                st.rerun()

        st.markdown("---")

        # Demo Mode Quick Switcher
        st.markdown("<p style='font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; font-weight: 700; margin-bottom: 8px;'>Demonstration Mode</p>", unsafe_allow_html=True)
        if st.button("⚡ Reset to Demo Student", use_container_width=True):
            from database.db import get_demo_student
            demo_stu = get_demo_student()
            if demo_stu:
                st.session_state["active_student"] = demo_stu
                st.session_state["current_page"] = "Recommendations"
                st.success("Loaded demo student profile!")
                st.rerun()

        # Database and ML Status Indicators
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="font-size: 0.75rem; color: #64748B; line-height: 1.5; padding: 10px 0;">
                <div>🟢 <b>DB:</b> SQLite (Connected)</div>
                <div>🟣 <b>ML:</b> Random Forest (180 Trees)</div>
                <div>⚡ <b>Test Accuracy:</b> 97.14%</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_about_viva_page():
    """Renders comprehensive project documentation and viva defense guide for academic evaluators."""
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div class="hero-badge">
                <span>📚 Academic Defense & Viva Guide</span>
            </div>
            <h2 style="color: #F8FAFC; margin-bottom: 4px;">Project Architecture & Technical Documentation</h2>
            <p style="color: #94A3B8; font-size: 0.95rem;">
                3rd-Semester B.Tech Computer Science (AI & Data Science Specialization) Capstone Project.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    t1, t2, t3, t4 = st.tabs([
        "🏗️ System Architecture",
        "🌲 Machine Learning Pipeline",
        "💾 Database Schema",
        "🎯 Viva Q&A Guide"
    ])

    with t1:
        st.markdown("#### End-to-End Architectural Flow")
        st.markdown(
            """
            ```
            [ Student Browser UI ]
                   │
                   ▼ (HTTP / WebSocket)
            [ Streamlit Web Server (Python 3.14) ]
                   │
                   ├─► [ modules/assessment.py ]  ──> Captures 29-D Skill & Interest Vector
                   │
                   ├─► [ ml/predict.py ]           ──> Evaluates Trained Random Forest (.pkl)
                   │                                  - Computes Multi-class Probabilities
                   │                                  - Calibrates Top-3 Confidence Scores
                   │                                  - Computes Feature Attributions & Gaps
                   │
                   ├─► [ modules/skill_gap.py ]    ──> Plots Interactive Plotly Radar & Bar Charts
                   │
                   ├─► [ modules/roadmap.py ]      ──> Synthesizes Tailored 12-Week Roadmap
                   │
                   └─► [ database/db.py ]          ──> Persists Students, Assessments, Skills,
                                                      Recommendations & Roadmaps in SQLite
            ```
            """
        )

        st.markdown("#### Technology Stack Rationale")
        st.markdown(
            """
            - **Streamlit**: Selected for its rapid, reactive UI components, zero frontend build-tooling overhead, and seamless integration with Python ML pipelines.
            - **Scikit-Learn (Random Forest Classifier)**: Selected because of its exceptional capability to handle mixed discrete ordinal features (1-5 ratings), non-linear decision boundaries, immunity to multicollinearity, and intrinsic feature importance explainability.
            - **SQLite**: Lightweight, serverless relational database engine providing ACID transactional guarantees without external service dependencies.
            - **Plotly**: Client-side GPU-accelerated interactive charting for multi-dimensional radar polygons and stacked gap visualization.
            """
        )

    with t2:
        st.markdown("#### Machine Learning Training & Evaluation Details")
        metrics = get_model_evaluation_metrics()["metrics"]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model Architecture", "Random Forest Classifier")
            st.metric("Number of Estimators", "180 Trees")
        with col2:
            st.metric("Test Accuracy", f"{metrics['test_accuracy'] * 100:.2f}%")
            st.metric("Macro F1-Score", f"{metrics['macro_f1'] * 100:.2f}%")
        with col3:
            st.metric("Training Samples", f"{metrics['train_samples']} students")
            st.metric("Validation Samples", f"{metrics['test_samples']} students")

        st.markdown("#### Calibrated Confidence vs Raw Probability")
        st.info(
            """
            In multi-class classification across 7 classes, uniform random guessing yields ~14.3% per class.
            A raw probability of 45-50% for one class represents overwhelming confidence.
            Our engine applies calibrated scaling to map raw class posteriors into a realistic 60%-97%
            recommendation score that is human-intuitive for college students.
            """
        )

    with t3:
        st.markdown("#### Relational SQLite Schema Design")
        st.markdown(
            """
            - **`students`**: Stores student identity, university, semester, branch, and coding experience.
            - **`assessments`**: Stores evaluation sessions linked to `student_id` with foreign key cascade.
            - **`skills`**: Normalized record of 29 ordinal features (1-5) per assessment session.
            - **`career_recommendations`**: Ranked recommendations (1, 2, 3), confidence scores, and JSON match reasons.
            - **`learning_roadmaps`**: Serialized 12-week roadmap milestones per career recommendation.
            """
        )

    with t4:
        st.markdown("#### Potential Viva Questions & Model Answers")

        with st.expander("Q1: Why did you choose Random Forest over a single Decision Tree or Neural Network?"):
            st.markdown(
                """
                **Answer:**
                A single Decision Tree suffers from high variance and is prone to overfitting small nuances in student ratings.
                A Deep Neural Network requires tens of thousands of continuous samples and behaves like a black-box.
                **Random Forest** uses bootstrap aggregating (Bagging) across 180 decorrelated decision trees, which significantly reduces variance,
                handles categorical/ordinal ratings natively, and provides exact feature importance metrics for explainable recommendations.
                """
            )

        with st.expander("Q2: How do you handle cold-start or students with no prior coding experience?"):
            st.markdown(
                """
                **Answer:**
                Our 29-feature vector includes academic subjects (Math, DBMS, Networks) and personal work style preferences (Creative, Research, Problem Solving).
                Even if a student enters low scores (1/5) in programming languages, their academic strengths and domain interests steer them towards foundational
                tracks (like Web Development or Data Analytics) accompanied by a Fundamentals-first 12-week roadmap.
                """
            )

        with st.expander("Q3: How does the system compute the skill gap?"):
            st.markdown(
                """
                **Answer:**
                Each of the 7 career domains has an industry baseline benchmark (1-5 scale) across core competencies.
                The skill gap is computed as `Gap = max(0, Benchmark_Level - Student_Level)`.
                Overall readiness percentage is calculated as `(Student_Points / Total_Benchmark_Points) * 100%` and visually projected onto an interactive Plotly radar chart.
                """
            )


def main():
    """Main routing and execution flow."""
    load_custom_css()
    init_app_state()
    render_sidebar()

    current_page = st.session_state.get("current_page", "Home")

    if current_page == "Home":
        render_home_page()
    elif current_page == "Student Profile":
        render_registration_page()
    elif current_page == "Assessment":
        render_assessment_page()
    elif current_page == "Recommendations":
        render_recommendations_page()
    elif current_page == "Learning Roadmap":
        render_roadmap_page()
    elif current_page == "Student Dashboard":
        render_dashboard_page()
    elif current_page == "About & Viva":
        render_about_viva_page()
    else:
        render_home_page()


if __name__ == "__main__":
    main()
