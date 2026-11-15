"""
Career Recommendations and Detailed Results Module for CareerPath AI
Displays Top 3 Recommended Career Domains with:
- Calibrated match confidence scores (%)
- Transparent explainability ("Why this career matches you")
- Required skills vs Current skills
- Missing skill gaps
- Suggested beginner capstone projects
- Curated learning resources
- Embedded interactive Skill Gap Analysis (Plotly radar & bar charts)
"""

import streamlit as st
import json
from modules.skill_gap import create_radar_chart, create_gap_bar_chart
from modules.roadmap import get_roadmap_for_career
from database.db import get_latest_assessment, get_assessment_details


def render_recommendations_page():
    """Renders the top-3 career recommendations and deep-dive analytics."""
    active_student = st.session_state.get("active_student")

    if not active_student:
        st.warning("⚠️ No active student selected. Please register or select a student.")
        if st.button("Go to Student Registration"):
            st.session_state["current_page"] = "Student Profile"
            st.rerun()
        return

    # Check if we have recommendations in session state or need to load from DB
    recs = st.session_state.get("latest_recommendations")
    student_inputs = st.session_state.get("latest_student_inputs")

    if not recs:
        # Try loading latest assessment from database
        latest_meta = get_latest_assessment(active_student["student_id"])
        if latest_meta:
            details = get_assessment_details(latest_meta["assessment_id"])
            if details and details["recommendations"]:
                # Reconstruct recommendation objects
                from ml.predict import predict_top_careers
                student_inputs = details["skills"]
                # Filter student inputs to features
                from ml.preprocessing import FEATURE_COLS
                clean_inputs = {k: student_inputs.get(k, 1) for k in FEATURE_COLS}
                recs = predict_top_careers(clean_inputs, top_k=3)
                st.session_state["latest_recommendations"] = recs
                st.session_state["latest_student_inputs"] = clean_inputs

    if not recs:
        st.info("ℹ️ No assessment found for this student. Please take the assessment first to generate recommendations.")
        if st.button("🚀 Start Assessment Now"):
            st.session_state["current_page"] = "Assessment"
            st.rerun()
        return

    # Header
    st.markdown(
        f"""
        <div style="margin-bottom: 20px;">
            <div class="hero-badge">
                <span>🎯 Machine Learning Results</span>
            </div>
            <h2 style="color: #F8FAFC; margin-bottom: 4px;">Career Recommendations for {active_student['full_name']}</h2>
            <p style="color: #94A3B8; font-size: 0.95rem;">
                Based on your technical proficiencies, interests, and academic background, here are your top 3 recommended career domains.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Top 3 Recommendation Cards Overview
    st.markdown("### 🏆 Top 3 Recommended Career Paths")

    c1, c2, c3 = st.columns(3)
    rec_cols = [c1, c2, c3]

    for idx, (col, r) in enumerate(zip(rec_cols, recs), start=1):
        with col:
            medal = "🥇" if idx == 1 else ("🥈" if idx == 2 else "🥉")
            border_highlight = "rgba(139, 92, 246, 0.7)" if idx == 1 else "rgba(148, 163, 184, 0.2)"
            st.markdown(
                f"""
                <div class="career-card" style="border: 2px solid {border_highlight};">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                        <span style="font-size: 2.2rem;">{r.get('icon', '🎯')}</span>
                        <div style="text-align: right;">
                            <span class="metric-pill {'pill-purple' if idx == 1 else 'pill-cyan'}">{medal} Rank #{idx}</span>
                            <div style="font-size: 1.4rem; font-weight: 800; color: #38BDF8; margin-top: 4px;">
                                {r.get('confidence_score', 85.0)}%
                            </div>
                            <span style="font-size: 0.72rem; color: #94A3B8;">Confidence Match</span>
                        </div>
                    </div>
                    <h3 style="color: #F8FAFC; margin-bottom: 4px; font-size: 1.25rem;">{r.get('career_title', 'Career Domain')}</h3>
                    <p style="color: #06B6D4; font-size: 0.8rem; font-weight: 600; margin-bottom: 10px;">{r.get('tagline', '')}</p>
                    <p style="color: #94A3B8; font-size: 0.84rem; line-height: 1.4; margin-bottom: 14px;">
                        {r.get('description', '')}
                    </p>
                    <div style="margin-top: 10px;">
                        <span style="font-size: 0.8rem; color: #CBD5E1; font-weight: 600;">Core Readiness:</span>
                        <div style="background: rgba(148, 163, 184, 0.2); border-radius: 8px; height: 8px; width: 100%; margin-top: 5px;">
                            <div style="background: linear-gradient(90deg, #8B5CF6, #06B6D4); width: {r.get('match_readiness_pct', 65.0)}%; height: 8px; border-radius: 8px;"></div>
                        </div>
                        <span style="font-size: 0.75rem; color: #94A3B8; float: right; margin-top: 3px;">{r.get('match_readiness_pct', 65.0)}% of required skills</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Detailed Career Inspection
    st.markdown("### 🔍 Deep Dive: Skill Gap, Projects & Learning Plan")

    career_titles = [r["career_title"] for r in recs]
    selected_career = st.selectbox(
        "Select Career to inspect details and skill gap:",
        career_titles,
        index=0
    )

    # Find the selected career object
    target_rec = next(r for r in recs if r["career_title"] == selected_career)

    tab_overview, tab_skillgap, tab_projects, tab_roadmap_view = st.tabs([
        f"📋 {target_rec['career_title']} Overview",
        "📊 Skill Gap Visualizations",
        "💡 Beginner Projects & Resources",
        "🗺️ 12-Week Roadmap Preview"
    ])

    with tab_overview:
        col_ov1, col_ov2 = st.columns([3, 2])

        with col_ov1:
            st.markdown(f"#### Why {target_rec['career_title']} matches your profile:")
            st.markdown(
                """
                <p style="color: #94A3B8; font-size: 0.9rem;">
                    Our Random Forest model evaluated your 29 individual assessment signals.
                    Here are the primary algorithmic factors driving this match:
                </p>
                """,
                unsafe_allow_html=True
            )
            for reason in target_rec["match_reasons"]:
                st.markdown(f"✅ **{reason}**")

            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
            st.markdown("#### Acquired vs Missing Competencies:")

            col_acq, col_miss = st.columns(2)
            with col_acq:
                st.markdown("##### 🟢 Strengths (Ready)")
                if target_rec["acquired_skills"]:
                    for s in target_rec["acquired_skills"]:
                        st.markdown(f"- **{s}**")
                else:
                    st.caption("No skills currently meet the target threshold.")

            with col_miss:
                st.markdown("##### 🟡 Gap Skills (To Develop)")
                if target_rec["missing_skills"]:
                    for s in target_rec["missing_skills"]:
                        st.markdown(f"- **{s}**")
                else:
                    st.success("All core prerequisites achieved!")

        with col_ov2:
            st.markdown("#### Match Intelligence Summary")
            st.markdown(
                f"""
                <div class="glass-card">
                    <p style="margin: 0; color: #94A3B8; font-size: 0.82rem;">CALIBRATED MATCH SCORE</p>
                    <h2 style="margin: 4px 0 10px 0; color: #38BDF8; font-size: 2.2rem;">{target_rec['confidence_score']}%</h2>
                    <p style="margin: 0; color: #94A3B8; font-size: 0.82rem;">MODEL RAW POSTERIOR PROBABILITY</p>
                    <h3 style="margin: 4px 0 10px 0; color: #C084FC;">{target_rec['raw_probability']}%</h3>
                    <p style="margin: 0; color: #94A3B8; font-size: 0.82rem;">CORE SKILL READINESS</p>
                    <h3 style="margin: 4px 0 10px 0; color: #10B981;">{target_rec['match_readiness_pct']}%</h3>
                    <hr style="border-color: rgba(148, 163, 184, 0.15); margin: 12px 0;">
                    <p style="font-size: 0.8rem; color: #94A3B8; line-height: 1.4;">
                        Confidence score indicates normalized affinity based on random forest tree votes and domain requirements.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab_skillgap:
        st.markdown("#### Module 6: Competency Comparison & Skill Gap Analysis")
        st.caption("Visualizing the delta between your self-reported competency (1-5) and the industry role baseline.")

        sg_col1, sg_col2 = st.columns([1, 1])

        with sg_col1:
            st.markdown("##### 🕸️ Skill Competency Radar (Spider Chart)")
            radar_fig = create_radar_chart(student_inputs, target_rec["career_title"])
            st.plotly_chart(radar_fig, use_container_width=True)

        with sg_col2:
            st.markdown("##### 📊 Skill Gap Breakdown")
            bar_fig, gap_df = create_gap_bar_chart(student_inputs, target_rec["career_title"])
            st.plotly_chart(bar_fig, use_container_width=True)

        st.markdown("##### 📋 Detailed Competency Table")
        st.dataframe(
            gap_df[["Skill", "Current Level", "Target Level", "Gap Points", "Status"]],
            use_container_width=True,
            hide_index=True
        )

    with tab_projects:
        st.markdown(f"#### Suggested Beginner Projects for {target_rec['career_title']}")
        st.caption("Building these portfolio projects demonstrates practical competence to employers and professors:")

        p_cols = st.columns(3)
        for p_idx, (p_col, project_title) in enumerate(zip(p_cols, target_rec["beginner_projects"]), start=1):
            with p_col:
                st.markdown(
                    f"""
                    <div class="glass-card" style="height: 100%;">
                        <span class="metric-pill pill-purple">Project #{p_idx}</span>
                        <h4 style="color: #F8FAFC; margin-top: 8px; margin-bottom: 8px;">{project_title}</h4>
                        <p style="color: #94A3B8; font-size: 0.84rem;">
                            Covers core industry skills, data structures, and production-ready implementation practices.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("#### Curated Learning Resources")
        for res in target_rec["resources"]:
            st.markdown(
                f"""
                <div style="background: rgba(15, 23, 42, 0.5); padding: 12px 16px; border-radius: 8px; border: 1px solid rgba(148, 163, 184, 0.15); margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color: #F8FAFC; font-weight: 600;">{res['title']}</span>
                        <span class="metric-pill pill-cyan" style="margin-left: 10px;">{res['type']}</span>
                    </div>
                    <a href="{res['url']}" target="_blank" style="color: #C084FC; text-decoration: none; font-weight: 600; font-size: 0.9rem;">
                        Visit Resource ↗
                    </a>
                </div>
                """,
                unsafe_allow_html=True
            )

    with tab_roadmap_view:
        st.markdown(f"#### 12-Week Structured Learning Pathway for {target_rec['career_title']}")
        roadmap_steps = get_roadmap_for_career(target_rec["career_title"])

        for step in roadmap_steps:
            st.markdown(
                f"""
                <div class="roadmap-timeline-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <h4 style="color: #F8FAFC; margin: 0;">{step['phase']}</h4>
                        <span class="metric-pill pill-purple">{step['tag']} • {step['hours']}</span>
                    </div>
                    <p style="color: #38BDF8; font-size: 0.88rem; margin-bottom: 8px; font-weight: 500;">
                        {step['summary']}
                    </p>
                    <div style="color: #94A3B8; font-size: 0.82rem; margin-bottom: 6px;">
                        <b>Key Focus Areas:</b> {', '.join(step['topics'])}
                    </div>
                    <div style="color: #A7F3D0; font-size: 0.82rem;">
                        <b>Practical Coding Task:</b> {step['practical_task']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        if st.button("🗺️ View Full Interactive Roadmap Screen", use_container_width=True):
            st.session_state["selected_roadmap_career"] = target_rec["career_title"]
            st.session_state["current_page"] = "Learning Roadmap"
            st.rerun()
