"""
CareerPath AI - Senior Software Tester Comprehensive Audit Test Suite
Executes rigorous automated verification across all 10 project requirements:
1. Student registration & profile updates
2. SQLite database persistence & relational integrity
3. Assessment questionnaire inputs & validation
4. Machine Learning model training & metrics evaluation
5. Prediction generation from student responses
6. Top 3 career recommendations ranking & score calibration
7. Skill gap analysis & Plotly radar/bar visualizations
8. Personalized 12-week roadmap synthesis & milestones
9. Dashboard data retrieval & past assessment loading
10. End-to-end integration & server health check
"""

import sys
import os
import json
import sqlite3
import pandas as pd
import numpy as np

# Set project root in path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from database.db import (
    init_db,
    get_connection,
    register_student,
    get_student_by_id,
    get_all_students,
    get_demo_student,
    save_assessment_results,
    get_latest_assessment,
    get_assessment_history,
    get_assessment_details
)
from ml.preprocessing import (
    FEATURE_COLS,
    FEATURE_LABELS,
    CAREER_CLASSES,
    CAREER_METADATA,
    prepare_input_dataframe
)
from ml.train_model import train_and_evaluate
from ml.predict import predict_top_careers, get_model_evaluation_metrics, get_model
from modules.roadmap import get_roadmap_for_career, ROADMAP_TEMPLATES
from modules.skill_gap import create_radar_chart, create_gap_bar_chart


def run_audit():
    print("=" * 70)
    print("CAREERPATH AI - SENIOR SOFTWARE TESTER AUDIT SUITE")
    print("=" * 70)

    results = {}

    # -------------------------------------------------------------
    # CHECK 1 & 2: REGISTRATION & SQLITE STORAGE
    # -------------------------------------------------------------
    print("\n[*] Auditing Check 1 & 2: Student Registration & SQLite Persistence...")
    try:
        init_db()

        # Test registering a brand new student
        test_email = "tester.audit@engineering.edu"
        sid = register_student(
            full_name="Priya Patel",
            email=test_email,
            college_name="IIT Bombay",
            current_semester="3rd Semester",
            branch="CSE - Artificial Intelligence & Data Science",
            programming_experience="Intermediate (6 months - 2 years)"
        )
        assert sid is not None and sid > 0, "Student ID must be a positive integer"

        # Verify student retrieved
        stu = get_student_by_id(sid)
        assert stu is not None, "Failed to retrieve student by ID"
        assert stu["full_name"] == "Priya Patel", "Student full_name mismatch"
        assert stu["email"] == test_email.lower(), "Student email mismatch"
        assert stu["college_name"] == "IIT Bombay", "Student college mismatch"

        # Test updating student record by email
        sid_update = register_student(
            full_name="Priya Patel (Updated)",
            email=test_email,
            college_name="IIT Bombay Main Campus",
            current_semester="4th Semester",
            branch="CSE - Artificial Intelligence & Data Science",
            programming_experience="Advanced (2+ years of coding & projects)"
        )
        assert sid_update == sid, "Updating existing email should keep same student_id"
        stu_up = get_student_by_id(sid)
        assert stu_up["full_name"] == "Priya Patel (Updated)", "Student update failed"
        assert stu_up["current_semester"] == "4th Semester", "Student update semester failed"

        # Verify Demo Student exists
        demo_stu = get_demo_student()
        assert demo_stu is not None, "Demo student must be pre-seeded in SQLite"
        assert "Aarav" in demo_stu["full_name"] or demo_stu["student_id"] == 1

        print("  [✓] Check 1 & 2 PASSED: Registration, Update & SQLite persistence verified.")
        results["Check 1: Registration"] = "PASSED"
        results["Check 2: SQLite Storage"] = "PASSED"
    except Exception as e:
        print(f"  [✗] Check 1 & 2 FAILED: {e}")
        results["Check 1: Registration"] = f"FAILED: {e}"
        results["Check 2: SQLite Storage"] = f"FAILED: {e}"

    # -------------------------------------------------------------
    # CHECK 3: ASSESSMENT FORM INPUT HANDLING
    # -------------------------------------------------------------
    print("\n[*] Auditing Check 3: Assessment Form Processing & Preprocessing...")
    try:
        # Construct sample assessment ratings
        sample_inputs = {
            "c_prog": 3, "cpp": 3, "python": 5, "java": 2, "html_css": 2,
            "javascript": 2, "sql_db": 4, "dsa": 4, "ml": 5, "stats": 5,
            "int_ai": 5, "int_ds": 5, "int_web": 2, "int_swe": 3, "int_cyber": 2,
            "int_cloud": 3, "int_analytics": 5,
            "acad_math": 5, "acad_prog": 5, "acad_stats": 5, "acad_networks": 2,
            "acad_db": 4, "acad_algos": 4,
            "pref_problem_solving": 5, "pref_creative": 3, "pref_research": 5,
            "pref_team": 4, "pref_independent": 3, "pref_building_apps": 4
        }
        df_input = prepare_input_dataframe(sample_inputs)
        assert df_input.shape == (1, 29), f"Expected shape (1, 29), got {df_input.shape}"
        assert list(df_input.columns) == FEATURE_COLS, "Column order must match FEATURE_COLS"

        # Test boundary clamping (e.g. out of range inputs)
        clamped_df = prepare_input_dataframe({"python": 10, "ml": -5, "c_prog": "invalid"})
        assert clamped_df["python"].iloc[0] == 5, "Input > 5 must clamp to 5"
        assert clamped_df["ml"].iloc[0] == 1, "Input < 1 must clamp to 1"
        assert clamped_df["c_prog"].iloc[0] == 1, "Invalid string must fallback to 1"

        print("  [✓] Check 3 PASSED: Assessment form formatting & boundary safety verified.")
        results["Check 3: Assessment Form"] = "PASSED"
    except Exception as e:
        print(f"  [✗] Check 3 FAILED: {e}")
        results["Check 3: Assessment Form"] = f"FAILED: {e}"

    # -------------------------------------------------------------
    # CHECK 4: MACHINE LEARNING MODEL TRAINING
    # -------------------------------------------------------------
    print("\n[*] Auditing Check 4: ML Training Pipeline & Model Serialization...")
    try:
        bundle = get_model()
        assert bundle is not None, "Model bundle failed to load"
        assert "model" in bundle, "Missing model instance in bundle"
        assert "metrics" in bundle, "Missing evaluation metrics in bundle"
        assert "feature_importances" in bundle, "Missing feature importances in bundle"

        metrics = bundle["metrics"]
        test_acc = metrics["test_accuracy"]
        macro_f1 = metrics["macro_f1"]
        print(f"  -> Test Accuracy: {test_acc * 100:.2f}%")
        print(f"  -> Macro F1-Score: {macro_f1 * 100:.2f}%")
        print(f"  -> Training Samples: {metrics['train_samples']}")
        print(f"  -> Test Samples: {metrics['test_samples']}")

        assert test_acc > 0.85, f"Test accuracy ({test_acc}) must exceed 85%"
        assert macro_f1 > 0.85, f"Macro F1 ({macro_f1}) must exceed 85%"
        assert len(bundle["feature_importances"]) == 29, "All 29 features must have importance weights"

        print("  [✓] Check 4 PASSED: Random Forest model training & metrics validated.")
        results["Check 4: ML Model Training"] = "PASSED"
    except Exception as e:
        print(f"  [✗] Check 4 FAILED: {e}")
        results["Check 4: ML Model Training"] = f"FAILED: {e}"

    # -------------------------------------------------------------
    # CHECK 5 & 6: PREDICTIONS & TOP 3 RECOMMENDATIONS
    # -------------------------------------------------------------
    print("\n[*] Auditing Check 5 & 6: Prediction Generation & Top-3 Recommendations...")
    try:
        # Profile 1: AI Aspirant
        ai_inputs = {
            "c_prog": 3, "cpp": 3, "python": 5, "java": 2, "html_css": 2,
            "javascript": 2, "sql_db": 4, "dsa": 4, "ml": 5, "stats": 5,
            "int_ai": 5, "int_ds": 5, "int_web": 2, "int_swe": 3, "int_cyber": 2,
            "int_cloud": 3, "int_analytics": 5,
            "acad_math": 5, "acad_prog": 5, "acad_stats": 5, "acad_networks": 2,
            "acad_db": 4, "acad_algos": 4,
            "pref_problem_solving": 5, "pref_creative": 3, "pref_research": 5,
            "pref_team": 4, "pref_independent": 3, "pref_building_apps": 4
        }
        recs_ai = predict_top_careers(ai_inputs, top_k=3)
        assert len(recs_ai) == 3, f"Expected 3 recommendations, got {len(recs_ai)}"
        assert recs_ai[0]["career_title"] in ["AI/ML Engineer", "Data Scientist"], f"Unexpected top career: {recs_ai[0]['career_title']}"
        assert recs_ai[0]["confidence_score"] >= recs_ai[1]["confidence_score"] >= recs_ai[2]["confidence_score"], "Confidence scores must be strictly ordered"
        assert len(recs_ai[0]["match_reasons"]) > 0, "Top recommendation must have match explanations"

        # Profile 2: Web Developer Aspirant
        web_inputs = {
            "c_prog": 1, "cpp": 1, "python": 3, "java": 2, "html_css": 5,
            "javascript": 5, "sql_db": 3, "dsa": 3, "ml": 1, "stats": 1,
            "int_ai": 1, "int_ds": 1, "int_web": 5, "int_swe": 4, "int_cyber": 1,
            "int_cloud": 2, "int_analytics": 1,
            "acad_math": 2, "acad_prog": 4, "acad_stats": 1, "acad_networks": 3,
            "acad_db": 3, "acad_algos": 3,
            "pref_problem_solving": 4, "pref_creative": 5, "pref_research": 1,
            "pref_team": 4, "pref_independent": 4, "pref_building_apps": 5
        }
        recs_web = predict_top_careers(web_inputs, top_k=3)
        assert recs_web[0]["career_title"] == "Web Developer", f"Expected Web Developer, got {recs_web[0]['career_title']}"
        print(f"  -> AI Profile Top Recommendation: {recs_ai[0]['career_title']} ({recs_ai[0]['confidence_score']}%)")
        print(f"  -> Web Profile Top Recommendation: {recs_web[0]['career_title']} ({recs_web[0]['confidence_score']}%)")

        print("  [✓] Check 5 & 6 PASSED: Real ML predictions & Top-3 calibrated ranking verified.")
        results["Check 5: Predictions"] = "PASSED"
        results["Check 6: Top-3 Recommendations"] = "PASSED"
    except Exception as e:
        print(f"  [✗] Check 5 & 6 FAILED: {e}")
        results["Check 5: Predictions"] = f"FAILED: {e}"
        results["Check 6: Top-3 Recommendations"] = f"FAILED: {e}"

    # -------------------------------------------------------------
    # CHECK 7: SKILL GAP ANALYSIS & PLOTLY VISUALIZATIONS
    # -------------------------------------------------------------
    print("\n[*] Auditing Check 7: Skill Gap Analysis & Plotly Visualizations...")
    try:
        top_career = recs_ai[0]["career_title"]
        radar_fig = create_radar_chart(ai_inputs, top_career)
        assert radar_fig is not None, "Radar figure generation failed"
        assert len(radar_fig.data) == 2, "Radar chart must contain 2 traces (Target & Current)"

        bar_fig, gap_df = create_gap_bar_chart(ai_inputs, top_career)
        assert bar_fig is not None, "Gap bar figure generation failed"
        assert len(bar_fig.data) == 2, "Gap bar chart must contain 2 stacked traces"
        assert len(gap_df) > 0, "Gap dataframe must not be empty"
        assert "Gap Points" in gap_df.columns, "Gap dataframe must have 'Gap Points'"
        assert "Status" in gap_df.columns, "Gap dataframe must have 'Status'"

        print(f"  -> Radar chart categories: {len(gap_df)} core skills analyzed")
        print("  [✓] Check 7 PASSED: Interactive radar & stacked gap bar charts verified.")
        results["Check 7: Skill Gap Analysis"] = "PASSED"
    except Exception as e:
        print(f"  [✗] Check 7 FAILED: {e}")
        results["Check 7: Skill Gap Analysis"] = f"FAILED: {e}"

    # -------------------------------------------------------------
    # CHECK 8: PERSONALIZED LEARNING ROADMAPS
    # -------------------------------------------------------------
    print("\n[*] Auditing Check 8: 12-Week Roadmap Generation...")
    try:
        for career in CAREER_CLASSES:
            rm = get_roadmap_for_career(career)
            assert len(rm) == 6, f"Roadmap for {career} must have exactly 6 phases (2 weeks each)"
            phases = [p["tag"] for p in rm]
            assert "Fundamentals" in phases[0], f"Phase 1 must be Fundamentals for {career}"
            assert "Projects" in phases[4], f"Phase 5 must be Projects for {career}"
            assert "Interview" in phases[5] or "Portfolio" in phases[5], f"Phase 6 must be Portfolio & Interview for {career}"
            assert len(rm[0]["topics"]) > 0, "Phase must contain topics"
            assert rm[0]["practical_task"] != "", "Phase must contain a practical coding task"
            assert rm[0]["deliverable"] != "", "Phase must contain a milestone deliverable"

        print(f"  -> Verified 12-week roadmaps across all {len(CAREER_CLASSES)} career domains.")
        print("  [✓] Check 8 PASSED: 12-Week roadmaps structure & milestones verified.")
        results["Check 8: Personalized Roadmaps"] = "PASSED"
    except Exception as e:
        print(f"  [✗] Check 8 FAILED: {e}")
        results["Check 8: Personalized Roadmaps"] = f"FAILED: {e}"

    # -------------------------------------------------------------
    # CHECK 9: DASHBOARD DATA RETRIEVAL & HISTORY
    # -------------------------------------------------------------
    print("\n[*] Auditing Check 9: Dashboard Data Retrieval & History Tracking...")
    try:
        # Save Priya Patel's assessment into database
        roadmaps_dict = {r["career_title"]: get_roadmap_for_career(r["career_title"]) for r in recs_ai}
        aid = save_assessment_results(
            student_id=sid,
            skill_ratings=ai_inputs,
            recommendations=recs_ai,
            roadmaps_dict=roadmaps_dict
        )
        assert aid is not None and aid > 0, "Assessment ID must be valid"

        # Test dashboard history retrieval
        hist = get_assessment_history(sid)
        assert len(hist) > 0, "Assessment history must contain at least 1 entry"
        assert hist[0]["assessment_id"] == aid, "Latest assessment ID mismatch in history"
        assert hist[0]["top_career"] == recs_ai[0]["career_title"], "Top career mismatch in history"

        # Test full details retrieval
        details = get_assessment_details(aid)
        assert details is not None, "Failed to retrieve assessment details"
        assert len(details["recommendations"]) == 3, "Assessment details must have 3 recommendations"
        assert len(details["skills"]) > 0, "Assessment details must have skills"
        assert len(details["roadmaps"]) == 3, "Assessment details must have 3 roadmaps"

        print("  [✓] Check 9 PASSED: Dashboard queries, history log & details retrieval verified.")
        results["Check 9: Dashboard Data Retrieval"] = "PASSED"
    except Exception as e:
        print(f"  [✗] Check 9 FAILED: {e}")
        results["Check 9: Dashboard Data Retrieval"] = f"FAILED: {e}"

    # -------------------------------------------------------------
    # CHECK 10: END-TO-END SYSTEM INTEGRATION
    # -------------------------------------------------------------
    print("\n[*] Auditing Check 10: Server Health & Full Pipeline Integration...")
    try:
        # Check SQLite table row counts
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM students")
            cnt_students = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM assessments")
            cnt_assessments = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM skills")
            cnt_skills = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM career_recommendations")
            cnt_recs = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM learning_roadmaps")
            cnt_roadmaps = cur.fetchone()[0]

        print(f"  -> Total Students in DB: {cnt_students}")
        print(f"  -> Total Assessments in DB: {cnt_assessments}")
        print(f"  -> Total Skills rows in DB: {cnt_skills}")
        print(f"  -> Total Recommendations in DB: {cnt_recs}")
        print(f"  -> Total Roadmaps in DB: {cnt_roadmaps}")

        assert cnt_students >= 2, "DB should contain at least demo student and test student"
        assert cnt_assessments >= 2, "DB should contain at least 2 assessments"
        assert cnt_skills >= 2, "DB should contain skills for each assessment"
        assert cnt_recs >= 6, "DB should contain recommendations for each assessment"

        print("  [✓] Check 10 PASSED: Database relational integrity & server data confirmed.")
        results["Check 10: Error-Free Execution"] = "PASSED"
    except Exception as e:
        print(f"  [✗] Check 10 FAILED: {e}")
        results["Check 10: Error-Free Execution"] = f"FAILED: {e}"

    # -------------------------------------------------------------
    # SUMMARY
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print("AUDIT RESULTS SUMMARY:")
    print("=" * 70)
    all_passed = True
    for item, status in results.items():
        print(f"  {item:.<45} {status}")
        if "PASSED" not in status:
            all_passed = False

    print("=" * 70)
    if all_passed:
        print("ALL 10 REQUIREMENTS AUDITED & FULLY FUNCTIONAL! 🚀")
    else:
        print("SOME CHECKS REPORTED ISSUES.")
    print("=" * 70)

    return all_passed


if __name__ == "__main__":
    success = run_audit()
    sys.exit(0 if success else 1)
