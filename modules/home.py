"""
Home Page Module for CareerPath AI
Displays hero section, value propositions, supported career domains,
system workflow, and quick-action buttons (Start Assessment, Try Demo).
"""

import streamlit as st
from ml.preprocessing import CAREER_METADATA


def render_home_page():
    """Renders the modern SaaS home page."""

    # Hero Section
    st.markdown(
        """
        <div style="text-align: center; padding: 25px 10px 35px 10px;">
            <div class="hero-badge">
                <span>⚡ B.Tech Computer Science AI & Data Science Project</span>
            </div>
            <h1 class="gradient-title">CareerPath AI</h1>
            <p style="font-size: 1.35rem; color: #C084FC; font-weight: 600; margin-top: -6px; margin-bottom: 12px;">
                Discover Your Potential. Choose Your Future.
            </p>
            <p class="gradient-subtitle" style="margin: 0 auto 28px auto;">
                An intelligent career guidance platform powered by machine learning.
                Analyze your technical proficiencies, interests, and academic background to receive
                personalized career recommendations, skill gap evaluations, and a 12-week learning roadmap.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Hero Action Buttons
    col_cta1, col_cta2, col_cta3 = st.columns([1, 1, 1])

    with col_cta1:
        if st.button("🚀 Start New Assessment", use_container_width=True):
            st.session_state["current_page"] = "Assessment"
            st.rerun()

    with col_cta2:
        if st.button("👤 Register / Switch Student", use_container_width=True):
            st.session_state["current_page"] = "Student Profile"
            st.rerun()

    with col_cta3:
        if st.button("⚡ Explore Demo Assessment", use_container_width=True):
            # Load demo student
            from database.db import get_demo_student
            demo_stu = get_demo_student()
            if demo_stu:
                st.session_state["active_student"] = demo_stu
                st.session_state["current_page"] = "Recommendations"
                st.rerun()

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    # Key Value Highlights
    st.markdown("### 🌟 Platform Capabilities")
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)

    with f_col1:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; height: 100%;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">🤖</div>
                <h4 style="color: #F8FAFC; margin-bottom: 6px;">Random Forest AI</h4>
                <p style="color: #94A3B8; font-size: 0.88rem; line-height: 1.4;">
                    Real Scikit-Learn ensemble model trained on 2,100+ multi-dimensional student vectors with 97%+ accuracy.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f_col2:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; height: 100%;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">🎯</div>
                <h4 style="color: #F8FAFC; margin-bottom: 6px;">Top-3 Ranking</h4>
                <p style="color: #94A3B8; font-size: 0.88rem; line-height: 1.4;">
                    Calculates calibrated confidence scores and provides transparent, evidence-based match explanations.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f_col3:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; height: 100%;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">📊</div>
                <h4 style="color: #F8FAFC; margin-bottom: 6px;">Skill Gap Analysis</h4>
                <p style="color: #94A3B8; font-size: 0.88rem; line-height: 1.4;">
                    Interactive Plotly spider radar charts comparing student competence against industry requirements.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with f_col4:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; height: 100%;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">🗺️</div>
                <h4 style="color: #F8FAFC; margin-bottom: 6px;">12-Week Roadmap</h4>
                <p style="color: #94A3B8; font-size: 0.88rem; line-height: 1.4;">
                    Curated week-by-week curriculum with beginner capstone projects, tasks, and verified learning resources.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # How it Works Section
    st.markdown("### 🔄 How The AI Recommendation System Works")
    step1, step2, step3, step4 = st.columns(4)

    with step1:
        st.markdown(
            """
            <div class="glass-card">
                <span class="metric-pill pill-purple">Step 01</span>
                <h4 style="color: #F8FAFC; margin-top: 6px;">Complete Assessment</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">
                    Rate your technical programming languages, subject knowledge, domain interests, and work preferences (1 to 5).
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step2:
        st.markdown(
            """
            <div class="glass-card">
                <span class="metric-pill pill-cyan">Step 02</span>
                <h4 style="color: #F8FAFC; margin-top: 6px;">ML Model Prediction</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">
                    Our trained Random Forest classifier evaluates your feature vector across 29 dimensions to compute probabilities.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step3:
        st.markdown(
            """
            <div class="glass-card">
                <span class="metric-pill pill-green">Step 03</span>
                <h4 style="color: #F8FAFC; margin-top: 6px;">Gap & Alignment</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">
                    Examine your skill readiness percentage, missing prerequisites, and radar charts for each recommended path.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with step4:
        st.markdown(
            """
            <div class="glass-card">
                <span class="metric-pill pill-purple">Step 04</span>
                <h4 style="color: #F8FAFC; margin-top: 6px;">Execute Roadmap</h4>
                <p style="color: #94A3B8; font-size: 0.85rem;">
                    Follow the tailored 12-week schedule divided into fundamentals, practical exercises, projects, and interview prep.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Supported Career Domains
    st.markdown("### 🎓 Supported Career Domains (7 Specialized Tracks)")
    st.markdown("<p style='color: #94A3B8; margin-top: -10px;'>Our AI model maps student profiles into high-demand technology specializations:</p>", unsafe_allow_html=True)

    domains = list(CAREER_METADATA.items())
    # Display in 2 rows
    row1 = domains[:4]
    row2 = domains[4:]

    cols1 = st.columns(4)
    for col, (name, meta) in zip(cols1, row1):
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="height: 100%;">
                    <div style="font-size: 1.8rem; margin-bottom: 6px;">{meta['icon']}</div>
                    <h4 style="color: #F8FAFC; margin-bottom: 4px;">{name}</h4>
                    <p style="color: #06B6D4; font-size: 0.78rem; font-weight: 600; margin-bottom: 8px;">{meta['tagline']}</p>
                    <p style="color: #94A3B8; font-size: 0.82rem; line-height: 1.35;">{meta['description'][:110]}...</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    cols2 = st.columns(3)
    for col, (name, meta) in zip(cols2, row2):
        with col:
            st.markdown(
                f"""
                <div class="glass-card" style="height: 100%;">
                    <div style="font-size: 1.8rem; margin-bottom: 6px;">{meta['icon']}</div>
                    <h4 style="color: #F8FAFC; margin-bottom: 4px;">{name}</h4>
                    <p style="color: #06B6D4; font-size: 0.78rem; font-weight: 600; margin-bottom: 8px;">{meta['tagline']}</p>
                    <p style="color: #94A3B8; font-size: 0.82rem; line-height: 1.35;">{meta['description'][:110]}...</p>
                </div>
                """,
                unsafe_allow_html=True
            )
