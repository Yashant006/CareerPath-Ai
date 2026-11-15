"""
Career Assessment Questionnaire Module for CareerPath AI
Presents multi-section intuitive rating questionnaire across:
A. Technical Skills (1-5)
B. Domain Interests (1-5)
C. Academic Subjects (1-5)
D. Personal Preferences & Work Style (1-5)
Includes preset scenario quick-fill buttons for fast testing and viva demonstration.
"""

import streamlit as st
from ml.predict import predict_top_careers
from modules.roadmap import get_roadmap_for_career
from database.db import save_assessment_results, get_all_students


def apply_preset(preset_name):
    """Applies quick presets to session state for demonstration."""
    presets = {
        "ai_ds": {
            "c_prog": 3, "cpp": 3, "python": 5, "java": 2, "html_css": 2,
            "javascript": 2, "sql_db": 4, "dsa": 4, "ml": 5, "stats": 5,
            "int_ai": 5, "int_ds": 5, "int_web": 2, "int_swe": 3, "int_cyber": 2, "int_cloud": 3, "int_analytics": 5,
            "acad_math": 5, "acad_prog": 5, "acad_stats": 5, "acad_networks": 2, "acad_db": 4, "acad_algos": 4,
            "pref_problem_solving": 5, "pref_creative": 3, "pref_research": 5, "pref_team": 4, "pref_independent": 3, "pref_building_apps": 4
        },
        "web_dev": {
            "c_prog": 2, "cpp": 2, "python": 3, "java": 2, "html_css": 5,
            "javascript": 5, "sql_db": 3, "dsa": 3, "ml": 1, "stats": 2,
            "int_ai": 2, "int_ds": 2, "int_web": 5, "int_swe": 4, "int_cyber": 2, "int_cloud": 3, "int_analytics": 2,
            "acad_math": 2, "acad_prog": 4, "acad_stats": 2, "acad_networks": 3, "acad_db": 4, "acad_algos": 3,
            "pref_problem_solving": 4, "pref_creative": 5, "pref_research": 2, "pref_team": 4, "pref_independent": 4, "pref_building_apps": 5
        },
        "cyber_sec": {
            "c_prog": 4, "cpp": 3, "python": 4, "java": 2, "html_css": 2,
            "javascript": 2, "sql_db": 3, "dsa": 3, "ml": 2, "stats": 2,
            "int_ai": 2, "int_ds": 2, "int_web": 2, "int_swe": 3, "int_cyber": 5, "int_cloud": 3, "int_analytics": 2,
            "acad_math": 3, "acad_prog": 4, "acad_stats": 3, "acad_networks": 5, "acad_db": 3, "acad_algos": 3,
            "pref_problem_solving": 5, "pref_creative": 2, "pref_research": 4, "pref_team": 3, "pref_independent": 5, "pref_building_apps": 4
        },
        "cloud_devops": {
            "c_prog": 3, "cpp": 2, "python": 4, "java": 3, "html_css": 2,
            "javascript": 2, "sql_db": 4, "dsa": 3, "ml": 2, "stats": 2,
            "int_ai": 2, "int_ds": 2, "int_web": 3, "int_swe": 4, "int_cyber": 3, "int_cloud": 5, "int_analytics": 3,
            "acad_math": 3, "acad_prog": 4, "acad_stats": 3, "acad_networks": 5, "acad_db": 5, "acad_algos": 3,
            "pref_problem_solving": 4, "pref_creative": 2, "pref_research": 3, "pref_team": 5, "pref_independent": 3, "pref_building_apps": 5
        }
    }

    if preset_name in presets:
        for k, v in presets[preset_name].items():
            st.session_state[f"assess_{k}"] = v
            st.session_state[f"form_{k}"] = v


def render_assessment_page():
    """Renders the comprehensive assessment form."""
    active_student = st.session_state.get("active_student")

    # If no active student, prompt or pick default
    if not active_student:
        all_s = get_all_students()
        if all_s:
            st.session_state["active_student"] = all_s[0]
            active_student = all_s[0]
        else:
            st.warning("⚠️ Please register a student profile before taking the assessment.")
            if st.button("Go to Student Registration"):
                st.session_state["current_page"] = "Student Profile"
                st.rerun()
            return

    st.markdown(
        f"""
        <div style="margin-bottom: 15px;">
            <div class="hero-badge">
                <span>📝 Multi-Dimensional Evaluation</span>
            </div>
            <h2 style="color: #F8FAFC; margin-bottom: 4px;">Career Assessment Questionnaire</h2>
            <p style="color: #94A3B8; font-size: 0.95rem;">
                Evaluating candidate: <b style="color: #C084FC;">{active_student['full_name']}</b> ({active_student['branch']})
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Quick Presets for instant Professor / Examiner demonstration
    st.markdown("##### ⚡ Quick Demonstration Presets (1-Click Fill)")
    p_col1, p_col2, p_col3, p_col4 = st.columns(4)
    with p_col1:
        if st.button("🤖 AI & Data Science Profile", use_container_width=True):
            apply_preset("ai_ds")
            st.rerun()
    with p_col2:
        if st.button("🌐 Full-Stack Web Profile", use_container_width=True):
            apply_preset("web_dev")
            st.rerun()
    with p_col3:
        if st.button("🛡️ Cybersecurity Profile", use_container_width=True):
            apply_preset("cyber_sec")
            st.rerun()
    with p_col4:
        if st.button("☁️ Cloud & DevOps Profile", use_container_width=True):
            apply_preset("cloud_devops")
            st.rerun()

    st.markdown("---")

    rating_help = "Rating Scale: 1 = None/Novice, 2 = Basic, 3 = Intermediate, 4 = Advanced, 5 = Expert"

    # Multi-tab or multi-expander questionnaire
    with st.form("career_assessment_form"):

        # ==========================================
        # SECTION A: TECHNICAL SKILLS
        # ==========================================
        st.markdown("### 💻 Section A: Technical Skills & Languages")
        st.caption(f"Rate your current practical hands-on proficiency in core programming languages and technical concepts. {rating_help}")

        tech_col1, tech_col2 = st.columns(2)
        with tech_col1:
            c_prog = st.slider("C Programming", 1, 5, value=st.session_state.get("assess_c_prog", 2), key="form_c_prog")
            cpp = st.slider("C++", 1, 5, value=st.session_state.get("assess_cpp", 2), key="form_cpp")
            python = st.slider("Python", 1, 5, value=st.session_state.get("assess_python", 4), key="form_python")
            java = st.slider("Java", 1, 5, value=st.session_state.get("assess_java", 2), key="form_java")
            html_css = st.slider("HTML / CSS", 1, 5, value=st.session_state.get("assess_html_css", 3), key="form_html_css")

        with tech_col2:
            javascript = st.slider("JavaScript", 1, 5, value=st.session_state.get("assess_javascript", 2), key="form_javascript")
            sql_db = st.slider("SQL & Relational Databases", 1, 5, value=st.session_state.get("assess_sql_db", 3), key="form_sql_db")
            dsa = st.slider("Data Structures & Algorithms", 1, 5, value=st.session_state.get("assess_dsa", 3), key="form_dsa")
            ml = st.slider("Machine Learning Concepts", 1, 5, value=st.session_state.get("assess_ml", 3), key="form_ml")
            stats = st.slider("Statistics & Probability", 1, 5, value=st.session_state.get("assess_stats", 3), key="form_stats")

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        # ==========================================
        # SECTION B: DOMAIN INTERESTS
        # ==========================================
        st.markdown("### 🎯 Section B: Domain Interests & Passions")
        st.caption("How interested are you in building projects or working professionally in each technology area? (1 = Low, 5 = Passionate)")

        int_col1, int_col2 = st.columns(2)
        with int_col1:
            int_ai = st.slider("Artificial Intelligence", 1, 5, value=st.session_state.get("assess_int_ai", 4), key="form_int_ai")
            int_ds = st.slider("Data Science", 1, 5, value=st.session_state.get("assess_int_ds", 4), key="form_int_ds")
            int_web = st.slider("Web Development", 1, 5, value=st.session_state.get("assess_int_web", 3), key="form_int_web")
            int_swe = st.slider("Software Engineering & Architecture", 1, 5, value=st.session_state.get("assess_int_swe", 3), key="form_int_swe")

        with int_col2:
            int_cyber = st.slider("Cybersecurity & Ethical Hacking", 1, 5, value=st.session_state.get("assess_int_cyber", 2), key="form_int_cyber")
            int_cloud = st.slider("Cloud Computing & DevOps", 1, 5, value=st.session_state.get("assess_int_cloud", 3), key="form_int_cloud")
            int_analytics = st.slider("Data Analytics & Business Intelligence", 1, 5, value=st.session_state.get("assess_int_analytics", 4), key="form_int_analytics")

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        # ==========================================
        # SECTION C: ACADEMIC INTERESTS
        # ==========================================
        st.markdown("### 📚 Section C: Academic Subjects & Theoretical Comfort")
        st.caption("How comfortable and enthusiastic are you with academic university coursework in these subjects? (1 = Struggle/Dislike, 5 = Excel/Enjoy)")

        acad_col1, acad_col2 = st.columns(2)
        with acad_col1:
            acad_math = st.slider("Mathematics (Discrete, Linear Algebra, Calculus)", 1, 5, value=st.session_state.get("assess_acad_math", 4), key="form_acad_math")
            acad_prog = st.slider("Programming Fundamentals & OOP", 1, 5, value=st.session_state.get("assess_acad_prog", 4), key="form_acad_prog")
            acad_stats = st.slider("Academic Statistics & Probability", 1, 5, value=st.session_state.get("assess_acad_stats", 4), key="form_acad_stats")

        with acad_col2:
            acad_networks = st.slider("Computer Networks & Protocols", 1, 5, value=st.session_state.get("assess_acad_networks", 3), key="form_acad_networks")
            acad_db = st.slider("Database Management Systems (DBMS)", 1, 5, value=st.session_state.get("assess_acad_db", 4), key="form_acad_db")
            acad_algos = st.slider("Design & Analysis of Algorithms", 1, 5, value=st.session_state.get("assess_acad_algos", 4), key="form_acad_algos")

        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

        # ==========================================
        # SECTION D: PERSONAL PREFERENCES
        # ==========================================
        st.markdown("### 🧩 Section D: Personal Preferences & Work Style")
        st.caption("Which work environments and problem types stimulate your highest productivity? (1 = Least Preferred, 5 = Highly Preferred)")

        pref_col1, pref_col2 = st.columns(2)
        with pref_col1:
            pref_problem_solving = st.slider("Analytical Problem Solving & Brain Teasers", 1, 5, value=st.session_state.get("assess_pref_problem_solving", 5), key="form_pref_problem_solving")
            pref_creative = st.slider("Creative Visual Design & User Experiences", 1, 5, value=st.session_state.get("assess_pref_creative", 3), key="form_pref_creative")
            pref_research = st.slider("Research, Reading Papers & Experimentation", 1, 5, value=st.session_state.get("assess_pref_research", 4), key="form_pref_research")

        with pref_col2:
            pref_team = st.slider("Cross-Functional Team Collaboration", 1, 5, value=st.session_state.get("assess_pref_team", 4), key="form_pref_team")
            pref_independent = st.slider("Autonomous Deep Work & Independent Execution", 1, 5, value=st.session_state.get("assess_pref_independent", 4), key="form_pref_independent")
            pref_building_apps = st.slider("Building Practical, User-Facing Software Products", 1, 5, value=st.session_state.get("assess_pref_building_apps", 5), key="form_pref_building_apps")

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        # Submit button
        submit_assessment = st.form_submit_button(
            "🧠 Analyze Profile & Generate Recommendations",
            use_container_width=True
        )

        if submit_assessment:
            student_inputs = {
                # Skills
                "c_prog": c_prog, "cpp": cpp, "python": python, "java": java, "html_css": html_css,
                "javascript": javascript, "sql_db": sql_db, "dsa": dsa, "ml": ml, "stats": stats,
                # Interests
                "int_ai": int_ai, "int_ds": int_ds, "int_web": int_web, "int_swe": int_swe,
                "int_cyber": int_cyber, "int_cloud": int_cloud, "int_analytics": int_analytics,
                # Academics
                "acad_math": acad_math, "acad_prog": acad_prog, "acad_stats": acad_stats,
                "acad_networks": acad_networks, "acad_db": acad_db, "acad_algos": acad_algos,
                # Preferences
                "pref_problem_solving": pref_problem_solving, "pref_creative": pref_creative,
                "pref_research": pref_research, "pref_team": pref_team,
                "pref_independent": pref_independent, "pref_building_apps": pref_building_apps
            }

            # 1. Run Machine Learning predictions
            with st.spinner("🤖 Evaluating skill profile with Random Forest Classifier..."):
                top_recommendations = predict_top_careers(student_inputs, top_k=3)

                # 2. Build roadmaps for the recommended careers
                roadmaps_dict = {}
                for rec in top_recommendations:
                    career_name = rec["career_title"]
                    roadmaps_dict[career_name] = get_roadmap_for_career(career_name)

                # 3. Store in SQLite Database
                assessment_id = save_assessment_results(
                    student_id=active_student["student_id"],
                    skill_ratings=student_inputs,
                    recommendations=top_recommendations,
                    roadmaps_dict=roadmaps_dict
                )

                # 4. Save to session state for immediate rendering
                st.session_state["latest_assessment_id"] = assessment_id
                st.session_state["latest_student_inputs"] = student_inputs
                st.session_state["latest_recommendations"] = top_recommendations
                st.session_state["latest_roadmaps"] = roadmaps_dict
                st.session_state["selected_career_for_details"] = top_recommendations[0]["career_title"]

                st.success("✅ Assessment analyzed and saved successfully! Generating recommendations...")
                st.session_state["current_page"] = "Recommendations"
                st.rerun()
