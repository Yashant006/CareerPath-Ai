"""
Machine Learning Training Pipeline for CareerPath AI
Trains a Random Forest Classifier on student skill and interest profiles.
Evaluates accuracy, macro/weighted F1, precision, recall, and generates
evaluation metrics for transparency and academic demonstration.
Saves model and artifacts to models/career_model.pkl.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib

try:
    from .preprocessing import FEATURE_COLS, CAREER_CLASSES, CAREER_METADATA
except (ImportError, ValueError):
    try:
        from preprocessing import FEATURE_COLS, CAREER_CLASSES, CAREER_METADATA
    except ImportError:
        from ml.preprocessing import FEATURE_COLS, CAREER_CLASSES, CAREER_METADATA

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "career_dataset.csv")
MODELS_DIR = os.path.join(os.path.dirname(BASE_DIR), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "career_model.pkl")


def generate_synthetic_dataset(num_samples_per_class=300, random_state=42):
    """
    Generates realistic synthetic dataset of student skill profiles across all 7 careers.
    Uses domain knowledge distributions with realistic variance and noise.
    """
    np.random.seed(random_state)
    records = []

    # Archetype profiles: mean values for each feature per career class
    archetypes = {
        "AI/ML Engineer": {
            # Skills
            "c_prog": 3.0, "cpp": 3.2, "python": 4.7, "java": 2.5, "html_css": 2.2,
            "javascript": 2.1, "sql_db": 3.4, "dsa": 4.1, "ml": 4.7, "stats": 4.3,
            # Interests
            "int_ai": 4.8, "int_ds": 4.2, "int_web": 2.1, "int_swe": 3.4, "int_cyber": 2.3, "int_cloud": 3.2, "int_analytics": 4.0,
            # Academics
            "acad_math": 4.6, "acad_prog": 4.6, "acad_stats": 4.4, "acad_networks": 2.8, "acad_db": 3.5, "acad_algos": 4.6,
            # Preferences
            "pref_problem_solving": 4.7, "pref_creative": 3.0, "pref_research": 4.4, "pref_team": 3.8, "pref_independent": 3.6, "pref_building_apps": 4.5
        },
        "Data Scientist": {
            "c_prog": 2.4, "cpp": 2.5, "python": 4.6, "java": 2.3, "html_css": 2.0,
            "javascript": 2.0, "sql_db": 4.3, "dsa": 3.4, "ml": 4.2, "stats": 4.8,
            "int_ai": 3.9, "int_ds": 4.8, "int_web": 1.9, "int_swe": 2.8, "int_cyber": 2.0, "int_cloud": 3.0, "int_analytics": 4.7,
            "acad_math": 4.7, "acad_prog": 4.2, "acad_stats": 4.8, "acad_networks": 2.5, "acad_db": 4.3, "acad_algos": 3.9,
            "pref_problem_solving": 4.6, "pref_creative": 2.9, "pref_research": 4.7, "pref_team": 3.6, "pref_independent": 3.7, "pref_building_apps": 3.8
        },
        "Data Analyst": {
            "c_prog": 2.0, "cpp": 2.0, "python": 3.8, "java": 2.1, "html_css": 2.6,
            "javascript": 2.4, "sql_db": 4.8, "dsa": 2.5, "ml": 2.6, "stats": 4.3,
            "int_ai": 2.7, "int_ds": 4.1, "int_web": 2.5, "int_swe": 2.7, "int_cyber": 2.1, "int_cloud": 2.9, "int_analytics": 4.9,
            "acad_math": 3.6, "acad_prog": 3.5, "acad_stats": 4.4, "acad_networks": 2.3, "acad_db": 4.7, "acad_algos": 2.8,
            "pref_problem_solving": 4.1, "pref_creative": 3.8, "pref_research": 3.4, "pref_team": 4.3, "pref_independent": 3.3, "pref_building_apps": 3.9
        },
        "Software Developer": {
            "c_prog": 3.9, "cpp": 4.4, "python": 4.1, "java": 4.4, "html_css": 2.8,
            "javascript": 3.1, "sql_db": 3.9, "dsa": 4.8, "ml": 2.3, "stats": 3.1,
            "int_ai": 3.0, "int_ds": 2.6, "int_web": 3.2, "int_swe": 4.8, "int_cyber": 2.9, "int_cloud": 3.4, "int_analytics": 2.5,
            "acad_math": 4.0, "acad_prog": 4.8, "acad_stats": 3.0, "acad_networks": 3.4, "acad_db": 4.0, "acad_algos": 4.8,
            "pref_problem_solving": 4.8, "pref_creative": 3.4, "pref_research": 3.2, "pref_team": 4.2, "pref_independent": 3.8, "pref_building_apps": 4.8
        },
        "Web Developer": {
            "c_prog": 2.2, "cpp": 2.3, "python": 3.2, "java": 2.4, "html_css": 4.8,
            "javascript": 4.8, "sql_db": 3.6, "dsa": 3.0, "ml": 2.0, "stats": 2.3,
            "int_ai": 2.5, "int_ds": 2.2, "int_web": 4.9, "int_swe": 3.8, "int_cyber": 2.5, "int_cloud": 3.2, "int_analytics": 2.8,
            "acad_math": 2.7, "acad_prog": 4.5, "acad_stats": 2.4, "acad_networks": 3.2, "acad_db": 3.8, "acad_algos": 3.2,
            "pref_problem_solving": 4.0, "pref_creative": 4.7, "pref_research": 2.6, "pref_team": 4.1, "pref_independent": 3.9, "pref_building_apps": 4.9
        },
        "Cybersecurity Analyst": {
            "c_prog": 4.1, "cpp": 3.8, "python": 4.2, "java": 2.7, "html_css": 2.3,
            "javascript": 2.4, "sql_db": 3.4, "dsa": 3.3, "ml": 2.2, "stats": 2.8,
            "int_ai": 2.6, "int_ds": 2.3, "int_web": 2.6, "int_swe": 3.2, "int_cyber": 4.9, "int_cloud": 3.6, "int_analytics": 2.6,
            "acad_math": 3.7, "acad_prog": 4.2, "acad_stats": 2.9, "acad_networks": 4.9, "acad_db": 3.6, "acad_algos": 3.6,
            "pref_problem_solving": 4.7, "pref_creative": 2.8, "pref_research": 4.1, "pref_team": 3.6, "pref_independent": 4.4, "pref_building_apps": 4.1
        },
        "Cloud Engineer": {
            "c_prog": 2.8, "cpp": 2.8, "python": 4.1, "java": 3.6, "html_css": 2.5,
            "javascript": 2.7, "sql_db": 4.1, "dsa": 3.5, "ml": 2.5, "stats": 2.9,
            "int_ai": 2.9, "int_ds": 2.7, "int_web": 3.3, "int_swe": 4.1, "int_cyber": 3.7, "int_cloud": 4.9, "int_analytics": 3.1,
            "acad_math": 3.4, "acad_prog": 4.3, "acad_stats": 3.0, "acad_networks": 4.7, "acad_db": 4.6, "acad_algos": 3.5,
            "pref_problem_solving": 4.4, "pref_creative": 3.1, "pref_research": 3.3, "pref_team": 4.3, "pref_independent": 3.7, "pref_building_apps": 4.6
        }
    }

    for career, profile in archetypes.items():
        for _ in range(num_samples_per_class):
            row = {}
            for col in FEATURE_COLS:
                mean = profile.get(col, 3.0)
                # Standard deviation of 0.65 with Gaussian noise
                val = np.random.normal(loc=mean, scale=0.65)
                # Add random occasional cross-interest noise
                if np.random.rand() < 0.08:
                    val += np.random.uniform(-1.0, 1.0)
                # Round and clamp between 1 and 5
                val = int(np.clip(np.round(val), 1, 5))
                row[col] = val

            row["career_target"] = career
            records.append(row)

    df = pd.DataFrame(records)
    # Shuffle dataset
    df = df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)
    return df


def train_and_evaluate(dataset_path=DATA_PATH, save_artifacts=True):
    """
    Loads or generates dataset, trains Random Forest Classifier,
    evaluates performance, and saves model bundle with joblib.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)

    if not os.path.exists(dataset_path):
        print(f"[*] Generating synthetic dataset with 2,100 student records at: {dataset_path}")
        df = generate_synthetic_dataset(num_samples_per_class=300, random_state=42)
        df.to_csv(dataset_path, index=False)
    else:
        print(f"[*] Loading existing dataset from: {dataset_path}")
        df = pd.read_csv(dataset_path)

    X = df[FEATURE_COLS]
    y = df["career_target"]

    # Stratified 80-20 Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print(f"[*] Training Random Forest Classifier on {len(X_train)} samples...")
    # Initialize Random Forest with balanced class weights and fixed seed
    rf = RandomForestClassifier(
        n_estimators=180,
        max_depth=14,
        min_samples_split=3,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    )

    rf.fit(X_train, y_train)

    # Predictions & Evaluation
    y_pred = rf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred, labels=CAREER_CLASSES).tolist()

    print(f"\n================ MODEL EVALUATION ================")
    print(f"Test Accuracy: {acc * 100:.2f}%")
    print(f"Macro F1-Score: {report['macro avg']['f1-score'] * 100:.2f}%")
    print(f"Weighted F1-Score: {report['weighted avg']['f1-score'] * 100:.2f}%")
    print("===================================================\n")

    # Feature Importances
    importances = dict(zip(FEATURE_COLS, rf.feature_importances_))
    sorted_importances = sorted(importances.items(), key=lambda x: x[1], reverse=True)

    model_bundle = {
        "model": rf,
        "feature_cols": FEATURE_COLS,
        "classes": list(rf.classes_),
        "metrics": {
            "test_accuracy": float(acc),
            "macro_f1": float(report["macro avg"]["f1-score"]),
            "weighted_f1": float(report["weighted avg"]["f1-score"]),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "classification_report": report,
            "confusion_matrix": cm
        },
        "feature_importances": dict(sorted_importances)
    }

    if save_artifacts:
        joblib.dump(model_bundle, MODEL_PATH)
        print(f"[✓] Model bundle successfully saved to: {MODEL_PATH}")

    return model_bundle


if __name__ == "__main__":
    train_and_evaluate()
