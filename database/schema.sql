-- CareerPath AI Database Schema
-- SQLite 3 Compatible

CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    college_name TEXT NOT NULL,
    current_semester TEXT NOT NULL,
    branch TEXT NOT NULL,
    programming_experience TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assessments (
    assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'Completed',
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS skills (
    skill_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    -- Technical Skills (1-5)
    c_prog INTEGER NOT NULL,
    cpp INTEGER NOT NULL,
    python INTEGER NOT NULL,
    java INTEGER NOT NULL,
    html_css INTEGER NOT NULL,
    javascript INTEGER NOT NULL,
    sql_db INTEGER NOT NULL,
    dsa INTEGER NOT NULL,
    ml INTEGER NOT NULL,
    stats INTEGER NOT NULL,
    -- Domain Interests (1-5)
    int_ai INTEGER NOT NULL,
    int_ds INTEGER NOT NULL,
    int_web INTEGER NOT NULL,
    int_swe INTEGER NOT NULL,
    int_cyber INTEGER NOT NULL,
    int_cloud INTEGER NOT NULL,
    int_analytics INTEGER NOT NULL,
    -- Academic Interests (1-5)
    acad_math INTEGER NOT NULL,
    acad_prog INTEGER NOT NULL,
    acad_stats INTEGER NOT NULL,
    acad_networks INTEGER NOT NULL,
    acad_db INTEGER NOT NULL,
    acad_algos INTEGER NOT NULL,
    -- Personal Preferences (1-5)
    pref_problem_solving INTEGER NOT NULL,
    pref_creative INTEGER NOT NULL,
    pref_research INTEGER NOT NULL,
    pref_team INTEGER NOT NULL,
    pref_independent INTEGER NOT NULL,
    pref_building_apps INTEGER NOT NULL,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS career_recommendations (
    recommendation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    career_rank INTEGER NOT NULL,
    career_title TEXT NOT NULL,
    confidence_score REAL NOT NULL,
    match_reasons TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS learning_roadmaps (
    roadmap_id INTEGER PRIMARY KEY AUTOINCREMENT,
    assessment_id INTEGER NOT NULL,
    career_title TEXT NOT NULL,
    roadmap_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id) ON DELETE CASCADE
);
