"""
Student Registration and Profile Management Module for CareerPath AI
Handles new student registration, profile updates, and active student session switching.
"""

import streamlit as st
import re
from database.db import register_student, get_all_students, get_student_by_id


def is_valid_email(email):
    """Simple regex validator for email format."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email.strip()) is not None


def render_registration_page():
    """Renders student registration and account switcher."""
    st.markdown(
        """
        <div style="margin-bottom: 20px;">
            <div class="hero-badge">
                <span>👤 Student Profile Management</span>
            </div>
            <h2 style="color: #F8FAFC; margin-bottom: 4px;">Student Registration & Profile</h2>
            <p style="color: #94A3B8; font-size: 0.95rem;">
                Register your academic profile or select an existing student account to track career assessments.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    tab_register, tab_existing = st.tabs(["📝 Register New Student / Edit Current", "🔄 Switch to Existing Profile"])

    with tab_register:
        # Check if there is an active student
        active_student = st.session_state.get("active_student")

        if active_student:
            st.info(f"Currently managing profile for: **{active_student['full_name']}** ({active_student['email']})")

        with st.form("student_registration_form"):
            st.markdown("#### Academic & Personal Details")

            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input(
                    "Full Name *",
                    value=active_student["full_name"] if active_student else "",
                    placeholder="e.g. Rahul Sharma"
                )
                email = st.text_input(
                    "Email Address *",
                    value=active_student["email"] if active_student else "",
                    placeholder="e.g. rahul.sharma@college.edu"
                )
                college_name = st.text_input(
                    "College / University Name *",
                    value=active_student["college_name"] if active_student else "Vellore Institute of Technology",
                    placeholder="e.g. National Institute of Technology"
                )

            with col2:
                semester_options = [
                    "1st Semester", "2nd Semester", "3rd Semester", "4th Semester",
                    "5th Semester", "6th Semester", "7th Semester", "8th Semester"
                ]
                current_sem_idx = 2
                if active_student and active_student.get("current_semester") in semester_options:
                    current_sem_idx = semester_options.index(active_student["current_semester"])

                current_semester = st.selectbox(
                    "Current Semester *",
                    semester_options,
                    index=current_sem_idx
                )

                branch_options = [
                    "Computer Science & Engineering (General)",
                    "CSE - Artificial Intelligence & Data Science",
                    "CSE - Cyber Security",
                    "Information Technology (IT)",
                    "Electronics & Communication Engineering",
                    "Electrical & Electronics Engineering",
                    "Other Engineering Stream"
                ]
                branch_idx = 1
                if active_student and active_student.get("branch") in branch_options:
                    branch_idx = branch_options.index(active_student["branch"])

                branch = st.selectbox(
                    "Branch / Major *",
                    branch_options,
                    index=branch_idx
                )

                exp_options = [
                    "Beginner (0 - 6 months)",
                    "Intermediate (6 months - 2 years)",
                    "Advanced (2+ years of coding & projects)",
                    "No prior programming experience"
                ]
                exp_idx = 1
                if active_student and active_student.get("programming_experience") in exp_options:
                    exp_idx = exp_options.index(active_student["programming_experience"])

                programming_experience = st.selectbox(
                    "Programming Experience Level *",
                    exp_options,
                    index=exp_idx
                )

            submitted = st.form_submit_button("💾 Save Profile & Proceed to Assessment", use_container_width=True)

            if submitted:
                if not full_name.strip():
                    st.error("Please enter your full name.")
                elif not email.strip() or not is_valid_email(email):
                    st.error("Please enter a valid email address.")
                elif not college_name.strip():
                    st.error("Please enter your college name.")
                else:
                    student_id = register_student(
                        full_name=full_name,
                        email=email,
                        college_name=college_name,
                        current_semester=current_semester,
                        branch=branch,
                        programming_experience=programming_experience
                    )
                    saved_student = get_student_by_id(student_id)
                    st.session_state["active_student"] = saved_student
                    st.success(f"Profile saved successfully for **{full_name}**! Redirecting...")
                    st.session_state["current_page"] = "Assessment"
                    st.rerun()

    with tab_existing:
        all_students = get_all_students()
        if not all_students:
            st.warning("No student profiles found in database yet. Register above to create one!")
        else:
            st.markdown("#### Select an existing student from SQLite database:")
            student_labels = {
                f"{s['full_name']} ({s['email']}) - {s['current_semester']}": s['student_id']
                for s in all_students
            }

            selected_label = st.selectbox("Select Student Profile:", list(student_labels.keys()))
            selected_id = student_labels[selected_label]

            col_s1, col_s2 = st.columns([1, 1])
            with col_s1:
                if st.button("✅ Switch to this Student", use_container_width=True):
                    st.session_state["active_student"] = get_student_by_id(selected_id)
                    st.success(f"Active student switched to {selected_label}!")
                    st.rerun()

            with col_s2:
                if st.button("📊 View Student Dashboard", use_container_width=True):
                    st.session_state["active_student"] = get_student_by_id(selected_id)
                    st.session_state["current_page"] = "Student Dashboard"
                    st.rerun()
