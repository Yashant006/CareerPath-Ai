"""
Preprocessing and Shared Constants for CareerPath AI ML System
Defines feature columns, career domains, skill requirements, and validation utilities.
"""

import pandas as pd
import numpy as np

# Exact feature names expected by the model
FEATURE_COLS = [
    # Technical Skills (1-5)
    "c_prog", "cpp", "python", "java", "html_css", "javascript", "sql_db", "dsa", "ml", "stats",
    # Domain Interests (1-5)
    "int_ai", "int_ds", "int_web", "int_swe", "int_cyber", "int_cloud", "int_analytics",
    # Academic Interests (1-5)
    "acad_math", "acad_prog", "acad_stats", "acad_networks", "acad_db", "acad_algos",
    # Personal Preferences (1-5)
    "pref_problem_solving", "pref_creative", "pref_research", "pref_team", "pref_independent", "pref_building_apps"
]

# Friendly labels for UI display
FEATURE_LABELS = {
    "c_prog": "C Programming",
    "cpp": "C++",
    "python": "Python",
    "java": "Java",
    "html_css": "HTML / CSS",
    "javascript": "JavaScript",
    "sql_db": "SQL & Databases",
    "dsa": "Data Structures & Algos",
    "ml": "Machine Learning",
    "stats": "Statistics & Probability",
    "int_ai": "Artificial Intelligence",
    "int_ds": "Data Science",
    "int_web": "Web Development",
    "int_swe": "Software Engineering",
    "int_cyber": "Cybersecurity",
    "int_cloud": "Cloud Computing",
    "int_analytics": "Data Analytics",
    "acad_math": "Mathematics",
    "acad_prog": "Programming Fundamentals",
    "acad_stats": "Academic Statistics",
    "acad_networks": "Computer Networks",
    "acad_db": "Database Systems",
    "acad_algos": "Algorithm Design",
    "pref_problem_solving": "Analytical Problem Solving",
    "pref_creative": "Creative UI/UX Design",
    "pref_research": "Research & Experimentation",
    "pref_team": "Team Collaboration",
    "pref_independent": "Independent Execution",
    "pref_building_apps": "Building Practical Apps"
}

CAREER_CLASSES = [
    "AI/ML Engineer",
    "Data Scientist",
    "Data Analyst",
    "Software Developer",
    "Web Developer",
    "Cybersecurity Analyst",
    "Cloud Engineer"
]

CAREER_METADATA = {
    "AI/ML Engineer": {
        "tagline": "Architect intelligent systems, neural networks, and automated learning algorithms.",
        "icon": "🤖",
        "color": "#8B5CF6",
        "description": "Designs, trains, and deploys high-performance machine learning models, neural networks, and AI pipelines to automate complex decision-making.",
        "core_skills": {"python": 5, "ml": 5, "dsa": 4, "stats": 4, "sql_db": 3, "cpp": 3},
        "academic_weights": {"acad_math": 5, "acad_algos": 5, "acad_stats": 4},
        "beginner_projects": [
            "Predictive Customer Churn Classifier with Scikit-Learn",
            "Computer Vision Image Classifier with PyTorch/TensorFlow",
            "Resume Keyword Matcher using NLP and Word Embeddings"
        ],
        "resources": [
            {"title": "Fast.ai: Practical Deep Learning for Coders", "type": "Free Course", "url": "https://course.fast.ai"},
            {"title": "Scikit-Learn Official User Guide", "type": "Documentation", "url": "https://scikit-learn.org"},
            {"title": "Deep Learning Specialization (Andrew Ng)", "type": "Course", "url": "https://deeplearning.ai"}
        ]
    },
    "Data Scientist": {
        "tagline": "Uncover hidden patterns, statistical anomalies, and predictive business insights.",
        "icon": "🔬",
        "color": "#3B82F6",
        "description": "Combines deep statistical analysis, scientific programming, and predictive algorithms to solve strategic problems and extract meaning from messy data.",
        "core_skills": {"python": 5, "stats": 5, "sql_db": 4, "ml": 4, "dsa": 3, "c_prog": 2},
        "academic_weights": {"acad_stats": 5, "acad_math": 5, "acad_db": 4},
        "beginner_projects": [
            "Exploratory Data Analysis on Real-World Healthcare Records",
            "Credit Card Fraud Detection with Imbalanced Data Sampling",
            "A/B Testing Statistical Simulator for Digital Conversion"
        ],
        "resources": [
            {"title": "StatQuest with Josh Starmer", "type": "Visual Lectures", "url": "https://statquest.org"},
            {"title": "Kaggle Micro-courses for Data Science", "type": "Hands-on", "url": "https://kaggle.com/learn"},
            {"title": "Python for Data Analysis (Wes McKinney)", "type": "O'Reilly Book", "url": "https://wesmckinney.com/book"}
        ]
    },
    "Data Analyst": {
        "tagline": "Translate raw metrics into high-impact dashboards and executive intelligence.",
        "icon": "📊",
        "color": "#06B6D4",
        "description": "Transforms relational databases, business logs, and operational telemetry into clear visual dashboards, KPI reports, and data-driven business decisions.",
        "core_skills": {"sql_db": 5, "stats": 4, "python": 4, "html_css": 2, "dsa": 2, "ml": 2},
        "academic_weights": {"acad_db": 5, "acad_stats": 4, "acad_math": 3},
        "beginner_projects": [
            "Interactive Sales Performance Dashboard with Plotly & Streamlit",
            "E-commerce Customer Retention & Cohort Churn Visualizer",
            "Hospitality Operations SQL Query & KPI Reporting Suite"
        ],
        "resources": [
            {"title": "Alex The Analyst Portfolio Bootcamp", "type": "Video Bootcamp", "url": "https://youtube.com"},
            {"title": "SQLZoo Interactive SQL Tutor", "type": "Interactive Guide", "url": "https://sqlzoo.net"},
            {"title": "Mode Analytics SQL & Python Guide", "type": "Handbook", "url": "https://mode.com"}
        ]
    },
    "Software Developer": {
        "tagline": "Engineer high-throughput distributed systems, algorithms, and resilient software.",
        "icon": "💻",
        "color": "#10B981",
        "description": "Designs, writes, optimizes, and tests reliable software architectures, object-oriented services, and multi-platform applications using modern design patterns.",
        "core_skills": {"dsa": 5, "cpp": 4, "java": 4, "python": 4, "sql_db": 4, "c_prog": 4},
        "academic_weights": {"acad_algos": 5, "acad_prog": 5, "acad_networks": 3},
        "beginner_projects": [
            "Multi-threaded HTTP Server in C++ or Java from Scratch",
            "RESTful Inventory Management API with JWT Authentication",
            "Distributed Key-Value Store with In-Memory Caching"
        ],
        "resources": [
            {"title": "NeetCode DSA Roadmap", "type": "Interactive Practice", "url": "https://neetcode.io"},
            {"title": "Refactoring Guru: Software Design Patterns", "type": "Visual Reference", "url": "https://refactoring.guru"},
            {"title": "GeeksforGeeks Algorithms Suite", "type": "Reference", "url": "https://geeksforgeeks.org"}
        ]
    },
    "Web Developer": {
        "tagline": "Craft sleek, responsive user interfaces, fluid web apps, and modern APIs.",
        "icon": "🌐",
        "color": "#F59E0B",
        "description": "Constructs dynamic, responsive web interfaces, full-stack web applications, and intuitive client-server communication channels using modern web protocols.",
        "core_skills": {"html_css": 5, "javascript": 5, "sql_db": 3, "python": 3, "dsa": 3, "java": 2},
        "academic_weights": {"acad_prog": 5, "acad_db": 4, "acad_networks": 3},
        "beginner_projects": [
            "Modern Responsive E-commerce Store with Cart & Checkout",
            "Real-time Collaborative Kanban Task Board with WebSockets",
            "Developer Portfolio Platform with Markdown CMS & Dark Mode"
        ],
        "resources": [
            {"title": "MDN Web Docs (Mozilla Developer Network)", "type": "Official Reference", "url": "https://developer.mozilla.org"},
            {"title": "The Odin Project Full-Stack Curriculum", "type": "Open-Source Course", "url": "https://theodinproject.com"},
            {"title": "Full Stack Open (University of Helsinki)", "type": "University Course", "url": "https://fullstackopen.com"}
        ]
    },
    "Cybersecurity Analyst": {
        "tagline": "Protect infrastructure, perform vulnerability assessments, and thwart adversaries.",
        "icon": "🛡️",
        "color": "#EF4444",
        "description": "Defends enterprise systems and digital infrastructure against threats, audits vulnerabilities, conducts penetration testing, and manages security policies.",
        "core_skills": {"c_prog": 4, "python": 4, "dsa": 3, "sql_db": 3, "cpp": 3, "html_css": 2},
        "academic_weights": {"acad_networks": 5, "acad_prog": 4, "acad_db": 3},
        "beginner_projects": [
            "Network Packet Sniffer & Protocol Analyzer with Scapy",
            "Web Application Security Scanner (OWASP Top 10 Checks)",
            "Automated Log Analyzer for Suspicious Authentication Bursts"
        ],
        "resources": [
            {"title": "TryHackMe: Pre-Security & SOC Analyst", "type": "Hands-on Lab", "url": "https://tryhackme.com"},
            {"title": "OverTheWire Bandit Wargames", "type": "Linux Challenges", "url": "https://overthewire.org"},
            {"title": "Professor Messer Security+ Training", "type": "Free Video Course", "url": "https://professormesser.com"}
        ]
    },
    "Cloud Engineer": {
        "tagline": "Build scalable cloud-native architectures, serverless backends, and DevOps pipelines.",
        "icon": "☁️",
        "color": "#6366F1",
        "description": "Architects, deploys, and orchestrates highly available cloud services, microservice clusters, automated CI/CD pipelines, and infrastructure as code.",
        "core_skills": {"python": 4, "sql_db": 4, "dsa": 3, "java": 3, "html_css": 2, "cpp": 2},
        "academic_weights": {"acad_networks": 5, "acad_db": 5, "acad_prog": 4},
        "beginner_projects": [
            "Serverless REST API Deployed on AWS Lambda / Google Cloud Functions",
            "Containerized Microservices Application with Docker & Nginx",
            "Automated Multi-Stage CI/CD Pipeline with GitHub Actions"
        ],
        "resources": [
            {"title": "AWS Hands-on Cloud Foundations", "type": "Workshops", "url": "https://aws.amazon.com/training"},
            {"title": "Docker & Kubernetes Official Guides", "type": "Hands-on Tutorials", "url": "https://kubernetes.io/docs"},
            {"title": "KodeKloud Cloud & DevOps Basics", "type": "Interactive Labs", "url": "https://kodekloud.com"}
        ]
    }
}


def prepare_input_dataframe(student_inputs_dict):
    """
    Validates and formats raw student input into a clean 1-row DataFrame matching FEATURE_COLS.
    Clamps any numerical inputs between 1 and 5.
    """
    row = {}
    for col in FEATURE_COLS:
        val = student_inputs_dict.get(col, 1)
        try:
            val = int(val)
        except (ValueError, TypeError):
            val = 1
        # Clamp to 1..5
        val = max(1, min(5, val))
        row[col] = val

    return pd.DataFrame([row], columns=FEATURE_COLS)
