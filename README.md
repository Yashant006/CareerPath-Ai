# CareerPath AI – Intelligent Career Recommendation System for Students

**Discover Your Potential. Choose Your Future.**

> **Academic Project:** 3rd-Semester B.Tech Computer Science & Engineering (Artificial Intelligence & Data Science Specialization).  
> **Built With:** Python 3, Streamlit, Scikit-learn, Pandas, NumPy, Joblib, SQLite, Plotly, HTML5/CSS3.

---

## 📖 1. Project Overview

**CareerPath AI** is a full-stack, machine-learning-powered career guidance web application designed specifically for engineering and computer science students. Rather than relying on rigid static rules or random quizzes, the platform evaluates a student's multi-dimensional profile across **29 distinct parameters**:

1. **Technical Skills (10 attributes):** C, C++, Python, Java, HTML/CSS, JavaScript, SQL & Databases, Data Structures & Algorithms, Machine Learning, Statistics.
2. **Domain Interests (7 attributes):** Artificial Intelligence, Data Science, Web Development, Software Engineering, Cybersecurity, Cloud Computing, Data Analytics.
3. **Academic Coursework Enthusiasm (6 attributes):** Mathematics, Programming Fundamentals, Academic Statistics, Computer Networks, DBMS, Algorithm Design.
4. **Personal Preferences & Work Style (6 attributes):** Analytical Problem Solving, Creative Visual Design, Research & Experimentation, Team Collaboration, Independent Work, Building Practical Software Products.

The system processes these parameters using a trained **Random Forest Classifier (180 Decision Trees)** to predict the top three recommended career domains, calculates calibrated match confidence scores (%), performs an interactive **Skill Gap Analysis** against industry benchmarks, and generates a personalized **12-week week-by-week learning roadmap** with beginner capstone projects and curated resources.

---

## 🌟 2. Key Features & Modules

* **Module 1: Home Page & Landing Experience**
  * Modern SaaS-style dark navy & purple gradient theme with responsive cards.
  * Platform overview, supported career domains, and a 4-step workflow breakdown.
  * One-click "Start New Assessment" and "Explore Demo Assessment" quick actions.

* **Module 2: Student Registration & Profile Management**
  * Captures student full name, university email, college, current semester, branch, and programming experience level.
  * Full relational storage in SQLite (`students` table) with support for switching accounts and profile updating.

* **Module 3: Multi-Dimensional Career Assessment**
  * Multi-section 1-to-5 Likert scale questionnaire.
  * **1-Click Demonstration Presets** (AI & Data Science, Web Dev, Cybersecurity, Cloud & DevOps) for instant examination and viva demonstrations.

* **Module 4: Machine Learning Recommendation Engine**
  * Real Scikit-learn **Random Forest Classifier** trained on 2,100 realistic student vectors across 7 target domains.
  * Achieves **97.14% Test Accuracy** and **97.15% Macro F1-score**.
  * Outputs ranked Top-3 career recommendations, calibrated match confidence percentages, and transparent feature attribution reasons.

* **Module 5: Career Recommendation Results**
  * Top-3 recommendation cards with rank badges (🥇, 🥈, 🥉), confidence scores, and core readiness indicators.
  * Transparent explainability: *"Why this career matches your profile"*.
  * Acquired competencies vs. missing skills breakdown.

* **Module 6: Skill Gap Analysis**
  * **Interactive Radar (Spider) Chart:** Overlays student competence against industry role benchmarks.
  * **Stacked Gap Bar Chart:** Highlights exact deficit points needed to reach professional competency.
  * Detailed numerical competency table.

* **Module 7: Personalized 12-Week Learning Roadmap**
  * Divided into six 2-week structured phases:
    * **Weeks 1–2:** Fundamentals
    * **Weeks 3–4:** Core technical skills
    * **Weeks 5–6:** Intermediate concepts
    * **Weeks 7–8:** Practical exercises
    * **Weeks 9–10:** Production capstone projects
    * **Weeks 11–12:** Portfolio and interview/viva preparation
  * Interactive checkbox milestone tracker and downloadable `.txt` study plan.

* **Module 8: Student Dashboard**
  * Central student record displaying past assessment dates, predicted careers, and progress.
  * History log stored in SQLite with full inspection capabilities.
  * Dedicated **ML System Transparency & Viva Guide** with live Gini feature importances.

* **Module 9: Database Architecture**
  * Relational SQLite schema with 5 tables (`students`, `assessments`, `skills`, `career_recommendations`, `learning_roadmaps`) with cascading foreign keys.

---

## 📁 3. Project Directory Structure

```
CareerPath-AI/
│
├── app.py                      # Main Streamlit application entry point & routing
├── requirements.txt            # Python package dependencies
├── README.md                   # Complete academic documentation & setup guide
│
├── database/
│   ├── __init__.py
│   ├── db.py                   # SQLite connection, CRUD transactions & seed logic
│   ├── schema.sql              # Relational SQL table definitions
│   └── careerpath.db           # SQLite database file (created on init)
│
├── ml/
│   ├── __init__.py
│   ├── preprocessing.py        # Feature schemas, labels, career metadata & constants
│   ├── train_model.py          # Model training pipeline, synthetic data generator & metrics
│   ├── predict.py              # Inference engine, probability calibration & explainability
│   └── career_dataset.csv      # 2,100 student skill training dataset
│
├── modules/
│   ├── __init__.py
│   ├── home.py                 # Module 1: Home page & value propositions
│   ├── registration.py         # Module 2: Registration & account switcher
│   ├── assessment.py           # Module 3: Multi-section 29-D questionnaire
│   ├── recommendation.py       # Module 5 & 6: Top-3 results & explainability
│   ├── skill_gap.py            # Module 6: Plotly radar & stacked bar charts
│   ├── roadmap.py              # Module 7: 12-week roadmap curriculum data
│   ├── roadmap_page.py         # Module 7: Interactive roadmap viewer & downloader
│   └── dashboard.py            # Module 8: Student dashboard & ML transparency
│
├── assets/
│   └── styles.css              # Dark navy & purple gradient SaaS stylesheet
│
└── models/
    └── career_model.pkl        # Serialized Random Forest model & evaluation bundle
```

---

## 💻 4. Technology Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend UI** | HTML5, CSS3, Streamlit | Modern dark navy & purple SaaS interface |
| **Backend** | Python 3.10+ / 3.14 | Application logic, routing, session management |
| **Machine Learning** | Scikit-learn, Pandas, NumPy, Joblib | Random Forest ensemble classifier (180 trees) |
| **Database** | SQLite 3 | Embedded ACID relational persistence |
| **Data Visualization** | Plotly Graph Objects & Express | Interactive radar charts & skill gap graphs |

---

## 🚀 5. How to Run in VS Code (Step-by-Step)

### Prerequisites
* Python 3.10 or higher installed on your system.
* VS Code (Visual Studio Code).

### Step 1: Open Project in VS Code
1. Open VS Code.
2. Click **File > Open Folder...** and select the `CareerPath-AI` directory:
   ```
   C:\Users\anila\.gemini\antigravity\scratch\CareerPath-AI
   ```

### Step 2: Open Terminal in VS Code
Open the integrated terminal in VS Code using the shortcut:
```
Ctrl + `  (backtick)
```
or click **Terminal > New Terminal** from the top menu.

### Step 3: Install Required Dependencies
Run the following command to install the required libraries:
```bash
pip install -r requirements.txt
```

### Step 4: (Optional) Re-train the Machine Learning Model
The model bundle is already pre-trained and saved in `models/career_model.pkl`. If you wish to retrain it from scratch or test the pipeline:
```bash
python ml/train_model.py
```
*Output will display the 97%+ accuracy score and classification report.*

### Step 5: Launch the Web Application
Start the Streamlit development server:
```bash
streamlit run app.py
```

VS Code will automatically launch your default web browser at:
```
http://localhost:8501
```

---

## 🧪 6. Testing & Demo Student Account

The database includes a pre-seeded student account for instantaneous testing during college viva:
* **Student Name:** Aarav Sharma (Demo Student)
* **Email:** `aarav.demo@university.edu`
* **College:** National Institute of Technology
* **Semester:** 3rd Semester
* **Branch:** Computer Science & Engineering (AI & Data Science)
* **Coding Experience:** Intermediate (1-2 years)

**Quick Demo Actions:**
1. Click **"⚡ Explore Demo Assessment"** on the home page or sidebar.
2. In the Assessment section, click any of the **Quick Presets** (e.g., *"🤖 AI & Data Science Profile"* or *"🌐 Full-Stack Web Profile"*) to automatically fill the 29 sliders in 1 second.
3. Click **"🧠 Analyze Profile & Generate Recommendations"** to see instant ML predictions, Plotly charts, and roadmaps.

---

## 🎓 7. Academic Viva Defense Guide (For College Professor)

### Q1: What machine learning algorithm is used, and why?
**Answer:** We implemented a **Random Forest Classifier** (`sklearn.ensemble.RandomForestClassifier`) with 180 estimators. Random Forest is an ensemble bagging method that builds multiple de-correlated decision trees. It is optimal for this problem because:
1. Student ratings are ordinal discrete features (1 to 5).
2. It handles non-linear relationships and interactions without requiring strict continuous distribution assumptions.
3. It resists overfitting through feature subsampling and bootstrap aggregation.
4. It provides transparent Gini feature importance calculations.

### Q2: How did you handle evaluation metrics?
**Answer:** The dataset of 2,100 student profiles was split into 80% training (1,680 samples) and 20% testing (420 samples) using **Stratified Sampling** to ensure equal class representation across all 7 career domains. The model was evaluated using:
* **Test Accuracy:** 97.14%
* **Macro F1-Score:** 97.15%
* **Weighted F1-Score:** 97.15%

### Q3: How do you differentiate between recommendation scores and raw probabilities?
**Answer:** In a 7-class classification problem, equal probability across all classes is $1/7 \approx 14.3\%$. A raw posterior probability of $45\%$ is statistically dominant. Presenting $45\%$ to a student could be misinterpreted as low suitability. Our prediction engine applies calibrated normalization so that the primary recommendation is scaled into a human-intuitive confidence score ($60\% - 97\%$).

---

## 📜 8. License
Developed for academic assessment in 3rd-Semester B.Tech Computer Science & Engineering (AI & Data Science). Open for educational and non-commercial learning.
