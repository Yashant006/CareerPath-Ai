"""
Dedicated Learning Roadmap Page for CareerPath AI
Renders the full interactive 12-week progression for any of the 7 career domains.
Allows students to track progress, inspect weekly tasks, milestones, deliverables,
and download their customized study schedule.
"""

import streamlit as st
from modules.roadmap import get_roadmap_for_career
from ml.preprocessing import CAREER_CLASSES, CAREER_METADATA


def render_roadmap_page():
    """Renders the full interactive 12-week learning roadmap page."""
    active_student = st.session_state.get("active_student")

    # Default career from session state or first class
    default_career = st.session_state.get("selected_roadmap_career")
    if not default_career:
        recs = st.session_state.get("latest_recommendations")
        if recs:
            default_career = recs[0]["career_title"]
        else:
            default_career = "AI/ML Engineer"

    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div class="hero-badge">
                <span>🗺️ Personalized Career Pathway</span>
            </div>
            <h2 style="color: #F8FAFC; margin-bottom: 4px;">12-Week Structured Learning Roadmap</h2>
            <p style="color: #94A3B8; font-size: 0.95rem;">
                Step-by-step curriculum with hands-on coding tasks, milestones, and interview preparation.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Career Selector
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        current_idx = CAREER_CLASSES.index(default_career) if default_career in CAREER_CLASSES else 0
        selected_career = st.selectbox(
            "Select Career Domain Roadmap:",
            CAREER_CLASSES,
            index=current_idx
        )
    with col_c2:
        meta = CAREER_METADATA.get(selected_career, {})
        st.markdown(
            f"""
            <div style="padding: 10px; background: rgba(30, 41, 59, 0.6); border-radius: 8px; border: 1px solid rgba(148, 163, 184, 0.2); margin-top: 18px;">
                <span style="font-size: 1.3rem;">{meta.get('icon', '🎯')}</span>
                <b style="color: #F8FAFC; margin-left: 6px;">{selected_career} Track</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    roadmap_steps = get_roadmap_for_career(selected_career)

    # Progress Summary
    st.markdown("#### ⏳ Roadmap Progression")

    # Checkboxes state in session
    completed_phases = 0
    total_phases = len(roadmap_steps)

    for i in range(total_phases):
        key = f"roadmap_{selected_career}_phase_{i}"
        if st.session_state.get(key, False):
            completed_phases += 1

    progress_pct = int((completed_phases / max(1, total_phases)) * 100)
    st.progress(progress_pct / 100.0)
    st.caption(f"Completed: {completed_phases} of {total_phases} phases ({progress_pct}%)")

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Render each of the 6 phases
    for idx, step in enumerate(roadmap_steps):
        phase_key = f"roadmap_{selected_career}_phase_{idx}"
        is_done = st.session_state.get(phase_key, False)

        with st.expander(f"{'✅ ' if is_done else '📌 '}{step['phase']} ({step['tag']})", expanded=(idx == 0 or not is_done)):
            c_left, c_right = st.columns([3, 1])

            with c_left:
                st.markdown(f"**Objective:** <span style='color: #38BDF8;'>{step['summary']}</span>", unsafe_allow_html=True)
                st.markdown("**Key Topics & Concepts:**")
                for topic in step["topics"]:
                    st.markdown(f"• {topic}")

                st.markdown(f"**💻 Practical Exercise:** <span style='color: #FDE047;'>{step['practical_task']}</span>", unsafe_allow_html=True)
                st.markdown(f"**📦 Milestone Deliverable:** <span style='color: #A7F3D0;'>{step['deliverable']}</span>", unsafe_allow_html=True)

            with c_right:
                st.markdown(f"<div class='glass-card' style='padding: 12px; text-align: center;'>", unsafe_allow_html=True)
                st.markdown(f"<span class='metric-pill pill-purple'>{step['tag']}</span>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #94A3B8; font-size: 0.8rem; margin: 8px 0 4px 0;'>ESTIMATED EFFORT</p>", unsafe_allow_html=True)
                st.markdown(f"<b style='color: #F8FAFC;'>{step['hours']}</b>", unsafe_allow_html=True)

                checked = st.checkbox("Mark as Completed", value=is_done, key=phase_key)
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Download Schedule as Text Plan
    plan_text = f"CAREERPATH AI - 12-WEEK LEARNING ROADMAP\n"
    plan_text += f"Target Domain: {selected_career}\n"
    if active_student:
        plan_text += f"Prepared for: {active_student['full_name']} ({active_student['email']})\n"
    plan_text += "=" * 60 + "\n\n"

    for step in roadmap_steps:
        plan_text += f"[{step['phase']}] - {step['tag']} ({step['hours']})\n"
        plan_text += f"Goal: {step['summary']}\n"
        plan_text += f"Topics: {', '.join(step['topics'])}\n"
        plan_text += f"Task: {step['practical_task']}\n"
        plan_text += f"Deliverable: {step['deliverable']}\n\n"

    st.download_button(
        label="📥 Download 12-Week Roadmap Plan (.txt)",
        data=plan_text,
        file_name=f"{selected_career.replace('/', '_').replace(' ', '_')}_Roadmap.txt",
        mime="text/plain",
        use_container_width=True
    )
