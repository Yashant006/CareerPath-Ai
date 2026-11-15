"""
Database Management Module for CareerPath AI
Handles SQLite initialization, CRUD operations for students, assessments,
skills, career recommendations, and learning roadmaps.
"""

import sqlite3
import os
import json
from datetime import datetime

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "careerpath.db")
SCHEMA_PATH = os.path.join(DB_DIR, "schema.sql")


def get_connection():
    """Returns a sqlite3 connection with Row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initializes database tables using schema.sql and seeds sample data if empty."""
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with get_connection() as conn:
        conn.executescript(schema_sql)
        conn.commit()

    seed_sample_students_if_empty()


def seed_sample_students_if_empty():
    """Seeds a demo student if the database is brand new so professors/students can test immediately."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM students")
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute(
                """
                INSERT INTO students (full_name, email, college_name, current_semester, branch, programming_experience)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    "Aarav Sharma (Demo Student)",
                    "aarav.demo@university.edu",
                    "National Institute of Technology",
                    "3rd Semester",
                    "Computer Science & Engineering (AI & Data Science)",
                    "Intermediate (1-2 years)"
                )
            )
            demo_student_id = cur.lastrowid

            # Add an assessment for demo student
            cur.execute(
                "INSERT INTO assessments (student_id, status) VALUES (?, ?)",
                (demo_student_id, "Completed")
            )
            demo_assessment_id = cur.lastrowid

            # Add demo skills
            cur.execute(
                """
                INSERT INTO skills (
                    assessment_id, c_prog, cpp, python, java, html_css, javascript, sql_db, dsa, ml, stats,
                    int_ai, int_ds, int_web, int_swe, int_cyber, int_cloud, int_analytics,
                    acad_math, acad_prog, acad_stats, acad_networks, acad_db, acad_algos,
                    pref_problem_solving, pref_creative, pref_research, pref_team, pref_independent, pref_building_apps
                ) VALUES (
                    ?, 3, 3, 5, 2, 3, 2, 4, 4, 4, 4,
                    5, 5, 2, 3, 2, 3, 5,
                    4, 5, 4, 2, 4, 5,
                    5, 3, 4, 4, 3, 5
                )
                """,
                (demo_assessment_id,)
            )

            # Add demo recommendations
            recs = [
                (demo_assessment_id, 1, "AI/ML Engineer", 94.2, json.dumps([
                    "High proficiency in Python (5/5) and Machine Learning (4/5)",
                    "Strong affinity for Mathematics (4/5) and Algorithms (5/5)",
                    "Passion for Artificial Intelligence and problem-solving"
                ])),
                (demo_assessment_id, 2, "Data Scientist", 88.7, json.dumps([
                    "Solid grasp of Statistics (4/5) and SQL Databases (4/5)",
                    "High interest in Data Analytics and Data Science",
                    "Appetite for research and mathematical problem solving"
                ])),
                (demo_assessment_id, 3, "Software Developer", 76.4, json.dumps([
                    "Competent in Data Structures & Algorithms (4/5)",
                    "Fundamental command of C/C++ and OOP concepts",
                    "Strong desire to build scalable software applications"
                ]))
            ]

            cur.executemany(
                """
                INSERT INTO career_recommendations (assessment_id, career_rank, career_title, confidence_score, match_reasons)
                VALUES (?, ?, ?, ?, ?)
                """,
                recs
            )

            # Pre-seed learning roadmaps for demo student
            try:
                from modules.roadmap import get_roadmap_for_career
                for c_title in ["AI/ML Engineer", "Data Scientist", "Software Developer"]:
                    cur.execute(
                        """
                        INSERT INTO learning_roadmaps (assessment_id, career_title, roadmap_json)
                        VALUES (?, ?, ?)
                        """,
                        (demo_assessment_id, c_title, json.dumps(get_roadmap_for_career(c_title)))
                    )
            except Exception as e:
                print(f"Notice: Demo roadmaps pre-population deferred: {e}")

            conn.commit()


def get_demo_student():
    """Finds the seeded demo student or the earliest registered student."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE LOWER(email) = 'aarav.demo@university.edu'")
        row = cur.fetchone()
        if row:
            return dict(row)
        cur.execute("SELECT * FROM students ORDER BY student_id ASC LIMIT 1")
        row = cur.fetchone()
        return dict(row) if row else None


def register_student(full_name, email, college_name, current_semester, branch, programming_experience):
    """Registers a new student or updates existing details by email."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT student_id FROM students WHERE LOWER(email) = LOWER(?)", (email.strip(),))
        existing = cur.fetchone()

        if existing:
            student_id = existing[0]
            cur.execute(
                """
                UPDATE students
                SET full_name = ?, college_name = ?, current_semester = ?, branch = ?, programming_experience = ?
                WHERE student_id = ?
                """,
                (full_name.strip(), college_name.strip(), current_semester, branch.strip(), programming_experience, student_id)
            )
        else:
            cur.execute(
                """
                INSERT INTO students (full_name, email, college_name, current_semester, branch, programming_experience)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (full_name.strip(), email.strip().lower(), college_name.strip(), current_semester, branch.strip(), programming_experience)
            )
            student_id = cur.lastrowid
        conn.commit()
        return student_id


def get_student_by_id(student_id):
    """Fetches student record by id."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def get_all_students():
    """Returns list of all students sorted by name."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY student_id DESC")
        return [dict(r) for r in cur.fetchall()]


def save_assessment_results(student_id, skill_ratings, recommendations, roadmaps_dict):
    """
    Saves a completed assessment, student's skill inputs, top 3 career recommendations,
    and roadmaps in a single atomic transaction.
    """
    with get_connection() as conn:
        cur = conn.cursor()

        # 1. Create assessment record
        cur.execute(
            "INSERT INTO assessments (student_id, status) VALUES (?, ?)",
            (student_id, "Completed")
        )
        assessment_id = cur.lastrowid

        # 2. Insert skills
        cur.execute(
            """
            INSERT INTO skills (
                assessment_id, c_prog, cpp, python, java, html_css, javascript, sql_db, dsa, ml, stats,
                int_ai, int_ds, int_web, int_swe, int_cyber, int_cloud, int_analytics,
                acad_math, acad_prog, acad_stats, acad_networks, acad_db, acad_algos,
                pref_problem_solving, pref_creative, pref_research, pref_team, pref_independent, pref_building_apps
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?
            )
            """,
            (
                assessment_id,
                skill_ratings.get("c_prog", 1),
                skill_ratings.get("cpp", 1),
                skill_ratings.get("python", 1),
                skill_ratings.get("java", 1),
                skill_ratings.get("html_css", 1),
                skill_ratings.get("javascript", 1),
                skill_ratings.get("sql_db", 1),
                skill_ratings.get("dsa", 1),
                skill_ratings.get("ml", 1),
                skill_ratings.get("stats", 1),

                skill_ratings.get("int_ai", 1),
                skill_ratings.get("int_ds", 1),
                skill_ratings.get("int_web", 1),
                skill_ratings.get("int_swe", 1),
                skill_ratings.get("int_cyber", 1),
                skill_ratings.get("int_cloud", 1),
                skill_ratings.get("int_analytics", 1),

                skill_ratings.get("acad_math", 1),
                skill_ratings.get("acad_prog", 1),
                skill_ratings.get("acad_stats", 1),
                skill_ratings.get("acad_networks", 1),
                skill_ratings.get("acad_db", 1),
                skill_ratings.get("acad_algos", 1),

                skill_ratings.get("pref_problem_solving", 1),
                skill_ratings.get("pref_creative", 1),
                skill_ratings.get("pref_research", 1),
                skill_ratings.get("pref_team", 1),
                skill_ratings.get("pref_independent", 1),
                skill_ratings.get("pref_building_apps", 1)
            )
        )

        # 3. Insert recommendations
        for rank, rec in enumerate(recommendations, start=1):
            cur.execute(
                """
                INSERT INTO career_recommendations (assessment_id, career_rank, career_title, confidence_score, match_reasons)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    assessment_id,
                    rank,
                    rec["career_title"],
                    float(rec["confidence_score"]),
                    json.dumps(rec.get("match_reasons", []))
                )
            )

        # 4. Insert roadmaps
        for career_name, roadmap_content in roadmaps_dict.items():
            cur.execute(
                """
                INSERT INTO learning_roadmaps (assessment_id, career_title, roadmap_json)
                VALUES (?, ?, ?)
                """,
                (assessment_id, career_name, json.dumps(roadmap_content))
            )

        conn.commit()
        return assessment_id


def get_latest_assessment(student_id):
    """Fetches the latest assessment ID and date for a student."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM assessments
            WHERE student_id = ?
            ORDER BY assessment_id DESC LIMIT 1
            """,
            (student_id,)
        )
        row = cur.fetchone()
        return dict(row) if row else None


def get_assessment_history(student_id):
    """Fetches all past assessments for a student with their top recommendation."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT a.assessment_id, a.submission_date, a.status,
                   cr.career_title as top_career, cr.confidence_score
            FROM assessments a
            LEFT JOIN career_recommendations cr ON a.assessment_id = cr.assessment_id AND cr.career_rank = 1
            WHERE a.student_id = ?
            ORDER BY a.assessment_id DESC
            """,
            (student_id,)
        )
        return [dict(r) for r in cur.fetchall()]


def get_assessment_details(assessment_id):
    """Fetches full assessment details including skills, recommendations, and roadmaps."""
    with get_connection() as conn:
        cur = conn.cursor()

        # Assessment info
        cur.execute("SELECT * FROM assessments WHERE assessment_id = ?", (assessment_id,))
        assessment_row = cur.fetchone()
        if not assessment_row:
            return None

        # Skills
        cur.execute("SELECT * FROM skills WHERE assessment_id = ?", (assessment_id,))
        skills_row = cur.fetchone()

        # Recommendations
        cur.execute(
            "SELECT * FROM career_recommendations WHERE assessment_id = ? ORDER BY career_rank ASC",
            (assessment_id,)
        )
        recs_rows = cur.fetchall()
        recs = []
        for r in recs_rows:
            d = dict(r)
            d["match_reasons"] = json.loads(d["match_reasons"]) if d["match_reasons"] else []
            recs.append(d)

        # Roadmaps
        cur.execute("SELECT * FROM learning_roadmaps WHERE assessment_id = ?", (assessment_id,))
        roadmap_rows = cur.fetchall()
        roadmaps = {}
        for r in roadmap_rows:
            roadmaps[r["career_title"]] = json.loads(r["roadmap_json"])

        return {
            "assessment": dict(assessment_row),
            "skills": dict(skills_row) if skills_row else {},
            "recommendations": recs,
            "roadmaps": roadmaps
        }
