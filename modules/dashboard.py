"""
Student Dashboard Module for CareerPath AI
Displays:
- Student Profile Information
- Assessment completion status & timestamp
- Top recommended careers summary
- Skill development progress
- Interactive roadmap progress tracker
- Previous assessment history log
- Academic viva evaluation summary (ML Metrics, Model transparency)
"""

import streamlit as st
import pandas as pd
from database.db import get_assessment_history, get_latest_assessment, get_assessment_details, get_all_students
from ml.predict import get_model_evaluation_metrics
from ml.preprocessing import FEATURE_LABELS


def render_dashboard_page():
    """Renders the comprehensive student dashboard."""
    active_student = st.session_state.get("active_student")

    if not active_student:
        all_s = get_all_students()
        if all_s:
            st.session_state["active_student"] = all_s[0]
            active_student = all_s[0]
        else:
            st.warning("⚠️ No student registered. Please register first.")
            if st.button("Register Student Profile"):
                st.session_state["current_page"] = "Student Profile"
                st.rerun()
            return

    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div class="hero-badge">
                <span>📊 Central Student Dashboard</span>
            </div>
            <h2 style="color: #F8FAFC; margin-bottom: 4px;">Student Overview: {active_student['full_name']}</h2>
            <p style="color: #94A3B8; font-size: 0.95rem;">
                Academic record, recommendation tracking, and skill progression history.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Top Metric Banner
    history = get_assessment_history(active_student["student_id"])
    total_assessments = len(history)
    latest_rec = history[0]["top_career"] if history and history[0].get("top_career") else "Not Assessed"
    latest_score = f"{history[0]['confidence_score']}%" if history and history[0].get("confidence_score") else "N/A"

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    with col_m1:
        st.markdown(
            f"""
            <div class="glass-card" style="padding: 16px;">
                <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">STUDENT ID / BRANCH</p>
                <h3 style="color: #F8FAFC; margin: 4px 0 0 0; font-size: 1.15rem;">#{active_student['student_id']}</h3>
                <span style="color: #38BDF8; font-size: 0.78rem;">{active_student['current_semester']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_m2:
        st.markdown(
            f"""
            <div class="glass-card" style="padding: 16px;">
                <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">ASSESSMENTS TAKEN</p>
                <h3 style="color: #C084FC; margin: 4px 0 0 0; font-size: 1.15rem;">{total_assessments} Completed</h3>
                <span style="color: #94A3B8; font-size: 0.78rem;">All records stored in SQLite</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_m3:
        st.markdown(
            f"""
            <div class="glass-card" style="padding: 16px;">
                <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">TOP PREDICTED CAREER</p>
                <h3 style="color: #10B981; margin: 4px 0 0 0; font-size: 1.15rem;">{latest_rec}</h3>
                <span style="color: #94A3B8; font-size: 0.78rem;">Confidence: {latest_score}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_m4:
        st.markdown(
            f"""
            <div class="glass-card" style="padding: 16px;">
                <p style="color: #94A3B8; font-size: 0.8rem; margin: 0;">CODING EXPERIENCE</p>
                <h3 style="color: #F59E0B; margin: 4px 0 0 0; font-size: 1.1rem;">{active_student['programming_experience'][:16]}...</h3>
                <span style="color: #94A3B8; font-size: 0.78rem;">Self-reported level</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Dashboard Tabs
    tab_profile, tab_history, tab_ml_metrics = st.tabs([
        "👤 Academic Profile Details",
        "📜 Assessment History & Reports",
        "🧠 Machine Learning Model Evaluation (For Viva/Professor)"
    ])

    with tab_profile:
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("#### Registered Student Information")
            st.markdown(
                f"""
                <div class="glass-card">
                    <p style="margin-bottom: 8px;"><b>Full Name:</b> <span style="color: #C084FC;">{active_student['full_name']}</span></p>
                    <p style="margin-bottom: 8px;"><b>Email Address:</b> {active_student['email']}</p>
                    <p style="margin-bottom: 8px;"><b>University:</b> {active_student['college_name']}</p>
                    <p style="margin-bottom: 8px;"><b>Semester:</b> {active_student['current_semester']}</p>
                    <p style="margin-bottom: 8px;"><b>Academic Branch:</b> {active_student['branch']}</p>
                    <p style="margin-bottom: 0px;"><b>Experience:</b> {active_student['programming_experience']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_p2:
            st.markdown("#### Quick Actions")
            st.markdown(
                """
                <div class="glass-card">
                    <p style="color: #94A3B8; font-size: 0.88rem;">
                        Perform regular assessments each semester to track your skill acquisition trajectory
                        and realign your 12-week study plan with evolving career opportunities.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("🚀 Retake / Update Career Assessment", use_container_width=True):
                st.session_state["current_page"] = "Assessment"
                st.rerun()

            if st.button("🎯 View Latest Recommendation Results", use_container_width=True):
                st.session_state["current_page"] = "Recommendations"
                st.rerun()

    with tab_history:
        st.markdown("#### Previous Assessments Log")
        if not history:
            st.info("No assessments recorded yet.")
        else:
            df_hist = pd.DataFrame(history)
            df_hist.rename(columns={
                "assessment_id": "Assessment ID",
                "submission_date": "Timestamp",
                "status": "Status",
                "top_career": "Top Predicted Career",
                "confidence_score": "Confidence Score (%)"
            }, inplace=True)

            st.dataframe(df_hist, use_container_width=True, hide_index=True)

            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            st.markdown("##### Inspect Past Assessment Details:")
            selected_aid = st.selectbox(
                "Select Assessment ID:",
                [h["assessment_id"] for h in history]
            )

            if st.button("Load Past Assessment Details"):
                past_details = get_assessment_details(selected_aid)
                if past_details:
                    from ml.predict import predict_top_careers
                    from ml.preprocessing import FEATURE_COLS
                    raw_skills = past_details.get("skills", {})
                    clean_inputs = {k: raw_skills.get(k, 1) for k in FEATURE_COLS}
                    reconstructed_recs = predict_top_careers(clean_inputs, top_k=3)

                    st.session_state["latest_assessment_id"] = selected_aid
                    st.session_state["latest_student_inputs"] = clean_inputs
                    st.session_state["latest_recommendations"] = reconstructed_recs
                    st.session_state["latest_roadmaps"] = past_details.get("roadmaps", {})
                    st.session_state["current_page"] = "Recommendations"
                    st.rerun()

    with tab_ml_metrics:
        st.markdown("#### Machine Learning System Transparency & Validation Metrics")
        st.caption("Demonstrating model evaluation, accuracy, and feature importances for viva defense and project inspection.")

        model_info = get_model_evaluation_metrics()
        metrics = model_info["metrics"]
        importances = model_info["feature_importances"]

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        with m_col1:
            st.metric("Test Accuracy", f"{metrics['test_accuracy'] * 100:.2f}%")
        with m_col2:
            st.metric("Macro F1-Score", f"{metrics['macro_f1'] * 100:.2f}%")
        with m_col3:
            st.metric("Weighted F1-Score", f"{metrics['weighted_f1'] * 100:.2f}%")
        with m_col4:
            st.metric("Dataset Records", f"{metrics['train_samples'] + metrics['test_samples']} rows")

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        st.markdown("##### 🌲 Top Predictive Features (Random Forest Feature Importances)")
        top_features = list(importances.items())[:12]
        feat_df = pd.DataFrame([
            {"Feature": FEATURE_LABELS.get(k, k), "Gini Importance Weight": v}
            for k, v in top_features
        ])

        import plotly.express as px
        fig_feat = px.bar(
            feat_df,
            x="Gini Importance Weight",
            y="Feature",
            orientation="h",
            color="Gini Importance Weight",
            color_continuous_scale="Purples"
        )
        fig_feat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(autorange="reversed", tickfont=dict(color='#E2E8F0')),
            xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', tickfont=dict(color='#94A3B8')),
            margin=dict(l=10, r=20, t=10, b=20),
            height=340
        )
        st.plotly_chart(fig_feat, use_container_width=True)

        st.info(
            """
            💡 **Viva Explanation Tip:**
            * The model utilizes a **Random Forest Classifier (Ensemble of 180 Decision Trees)** trained with balanced class weights.
            * Feature importance reflects the mean decrease in Gini impurity across all decision splits.
            * The system uses calibrated confidence scores based on tree vote distributions to distinguish between probability and relative recommendation strength.
            """
        )
