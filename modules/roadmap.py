"""
Personalized 12-Week Learning Roadmap Generator for CareerPath AI
Produces targeted, week-by-week learning pathways for each recommended career domain.
Divided into 6 structured phases (2 weeks each):
- Weeks 1-2: Fundamentals
- Weeks 3-4: Core Technical Skills
- Weeks 5-6: Intermediate Concepts
- Weeks 7-8: Practical Exercises
- Weeks 9-10: Capstone Projects
- Weeks 11-12: Portfolio & Interview Preparation
"""

ROADMAP_TEMPLATES = {
    "AI/ML Engineer": [
        {
            "phase": "Weeks 1–2: Mathematical Foundations & Advanced Python",
            "tag": "Fundamentals",
            "hours": "15-20 hrs/week",
            "summary": "Master linear algebra, vector spaces, calculus gradients, and vectorized Python computation with NumPy.",
            "topics": [
                "Matrix operations, eigenvalues, eigenvectors, and dot products",
                "Differential calculus: partial derivatives and gradient vectors",
                "Advanced Python: Generators, list comprehensions, decorators, and OOP",
                "NumPy array broadcasting, indexing, and vectorization"
            ],
            "practical_task": "Implement a linear algebra operations library from scratch using pure Python, then benchmark against NumPy.",
            "deliverable": "GitHub repository with mathematical benchmarks and vector computation proofs."
        },
        {
            "phase": "Weeks 3–4: Data Wrangling & Statistical Analysis",
            "tag": "Core Skills",
            "hours": "15-20 hrs/week",
            "summary": "Master Pandas data frames, data cleaning, handling missing data, and statistical probability distributions.",
            "topics": [
                "Pandas data transformation, grouping, merging, and reshaping",
                "Exploratory Data Analysis (EDA) and data visualization using Matplotlib and Seaborn",
                "Probability distributions (Gaussian, Binomial, Poisson)",
                "Hypothesis testing, p-values, confidence intervals, and z-tests"
            ],
            "practical_task": "Perform comprehensive end-to-end EDA on an imbalanced Kaggle dataset (e.g., Telecom Customer Churn).",
            "deliverable": "Interactive Jupyter Notebook report with statistical hypothesis conclusions."
        },
        {
            "phase": "Weeks 5–6: Classical Machine Learning & Scikit-Learn",
            "tag": "Intermediate Concepts",
            "hours": "18-22 hrs/week",
            "summary": "Understand core supervised and unsupervised algorithms, bias-variance tradeoff, and evaluation metrics.",
            "topics": [
                "Regression models (Linear, Ridge, Lasso) and cost functions",
                "Classification algorithms (Logistic Regression, Decision Trees, Random Forests, SVM)",
                "Clustering algorithms (K-Means, DBSCAN) and dimensionality reduction (PCA)",
                "Model evaluation: ROC-AUC, Precision-Recall curves, confusion matrices, and cross-validation"
            ],
            "practical_task": "Build, tune, and evaluate a Random Forest Classifier with GridSearchCV on a multi-class dataset.",
            "deliverable": "Validated ML classification pipeline with serialized `.joblib` model weights."
        },
        {
            "phase": "Weeks 7–8: Deep Learning & Neural Architectures",
            "tag": "Practical Exercises",
            "hours": "20-25 hrs/week",
            "summary": "Explore deep neural networks, backpropagation, activation functions, and PyTorch tensors.",
            "topics": [
                "Artificial Neural Networks (ANN), forward pass, and backpropagation mechanics",
                "Loss functions: Cross-Entropy, MSE, and optimization algorithms (Adam, RMSProp)",
                "Convolutional Neural Networks (CNN) for image recognition",
                "Transfer learning using pre-trained backbones (ResNet, MobileNet)"
            ],
            "practical_task": "Train a custom CNN in PyTorch to classify medical scans or satellite imagery with over 90% validation accuracy.",
            "deliverable": "PyTorch training script, loss curve visualization, and model checkpoint file."
        },
        {
            "phase": "Weeks 9–10: Production End-to-End Capstone Project",
            "tag": "Projects",
            "hours": "20-25 hrs/week",
            "summary": "Design and build a full-stack AI system with REST API inference, containerization, and interactive UI.",
            "topics": [
                "Serving ML models via FastAPI or Flask microservices",
                "Dockerizing model inference services for reproducible deployment",
                "Building an interactive frontend with Streamlit",
                "Input validation, error logging, and latency profiling"
            ],
            "practical_task": "Build an intelligent Resume Parsing and Skill Matcher application that processes PDFs and predicts candidate-job fit.",
            "deliverable": "Live hosted web application on Streamlit Cloud or Render with Dockerfile and GitHub README."
        },
        {
            "phase": "Weeks 11–12: MLOps, Portfolio & Viva Preparation",
            "tag": "Portfolio & Interview",
            "hours": "15-20 hrs/week",
            "summary": "Prepare for technical interviews, system design discussions, viva presentation, and GitHub polishing.",
            "topics": [
                "MLOps basics: Model versioning, drift detection, and MLflow tracking",
                "Explaining ML concepts in college viva and technical interviews",
                "Coding mock DSA rounds in Python (Arrays, Trees, Graphs)",
                "Structuring an ATS-optimized AI/ML Engineer resume and LinkedIn portfolio"
            ],
            "practical_task": "Record a 5-minute video walkthrough of your capstone project and document design choices in your README.",
            "deliverable": "Complete portfolio website, polished GitHub profile, and ready-to-present slide deck."
        }
    ],

    "Data Scientist": [
        {
            "phase": "Weeks 1–2: Python for Data Science & Advanced Statistics",
            "tag": "Fundamentals",
            "hours": "15-18 hrs/week",
            "summary": "Solidify Python data structures, probability theory, statistical inferences, and experimental design.",
            "topics": [
                "Descriptive statistics: mean, median, IQR, variance, and skewness",
                "Inferential statistics: Central Limit Theorem and sampling distributions",
                "Python object-oriented programming for analytics pipelines",
                "Data structures: sets, tuples, dictionaries, and time complexities"
            ],
            "practical_task": "Write a Python simulation that visually verifies the Central Limit Theorem across non-normal distributions.",
            "deliverable": "Executable script demonstrating sampling simulations with graphical plots."
        },
        {
            "phase": "Weeks 3–4: Advanced SQL & Data Engineering Basics",
            "tag": "Core Skills",
            "hours": "16-20 hrs/week",
            "summary": "Master complex SQL queries, window functions, CTEs, and relational database schema design.",
            "topics": [
                "Window functions: ROW_NUMBER(), RANK(), DENSE_RANK(), and NTILE()",
                "Common Table Expressions (CTEs), recursive queries, and self-joins",
                "Aggregation rollups, subqueries, and database indexing",
                "Connecting Python to SQLite and PostgreSQL via SQLAlchemy"
            ],
            "practical_task": "Solve 30 complex LeetCode / SQLZoo database questions covering cohort retention and revenue metrics.",
            "deliverable": "Documented SQL query notebook solving realistic business problems."
        },
        {
            "phase": "Weeks 5–6: Statistical Modeling & Exploratory Analytics",
            "tag": "Intermediate Concepts",
            "hours": "18-22 hrs/week",
            "summary": "Learn multivariate regression, feature engineering, statistical tests, and collinearity detection.",
            "topics": [
                "Multivariate Ordinary Least Squares (OLS) regression and assumptions",
                "Variance Inflation Factor (VIF) and multicollinearity mitigation",
                "Feature scaling, power transforms (Box-Cox, Yeo-Johnson), and outlier treatment",
                "ANOVA, Chi-Square test of independence, and Wilcoxon signed-rank tests"
            ],
            "practical_task": "Conduct a clinical or financial case study predicting outcomes with rigorous statistical hypothesis validation.",
            "deliverable": "Comprehensive statistical report with diagnostics plots and residual analysis."
        },
        {
            "phase": "Weeks 7–8: Machine Learning for Predictive Insights",
            "tag": "Practical Exercises",
            "hours": "18-22 hrs/week",
            "summary": "Implement ensemble algorithms, gradient boosted trees (XGBoost, LightGBM), and hyperparameter optimization.",
            "topics": [
                "Ensemble methods: Bagging, Boosting, and Stacking architectures",
                "XGBoost and LightGBM fundamentals, objective functions, and early stopping",
                "Hyperparameter tuning with Optuna or Bayesian Optimization",
                "Handling imbalanced data with SMOTE and class-weight balancing"
            ],
            "practical_task": "Train an XGBoost credit default prediction model with full SHAP value feature importance explainability.",
            "deliverable": "Trained predictive pipeline notebook with SHAP summary plots."
        },
        {
            "phase": "Weeks 9–10: A/B Testing & Capstone Data Product",
            "tag": "Projects",
            "hours": "20-25 hrs/week",
            "summary": "Design an experimental A/B testing framework and deploy a full interactive data science dashboard.",
            "topics": [
                "A/B test design: sample size calculation, statistical power, and minimum detectable effect",
                "Two-sample t-tests and Chi-Square proportion tests for conversion rates",
                "Interactive data science storytelling using Streamlit and Plotly",
                "Creating automated data pipelines that update visualizations"
            ],
            "practical_task": "Build an end-to-end Customer Lifetime Value (CLV) & Churn Prediction web application.",
            "deliverable": "Public Streamlit web application with dynamic sliders, predictive scores, and cohort visualizations."
        },
        {
            "phase": "Weeks 11–12: Storytelling, Portfolio & Interview Prep",
            "tag": "Portfolio & Interview",
            "hours": "15-18 hrs/week",
            "summary": "Translate complex models into executive business presentations, curate GitHub repos, and prepare for interviews.",
            "topics": [
                "Executive storytelling: Framing metrics as ROI and cost-reduction",
                "Data Science case-study interview frameworks (Metrics, Tradeoffs, Guardrails)",
                "Live coding practice: Pandas manipulation and SQL under time limits",
                "Crafting an impactful Data Science portfolio on Kaggle and GitHub"
            ],
            "practical_task": "Write an in-depth Medium or LinkedIn technical article explaining your capstone findings.",
            "deliverable": "Published technical article, cleaned GitHub repositories, and interview-ready resume."
        }
    ],

    "Data Analyst": [
        {
            "phase": "Weeks 1–2: Advanced Excel & Business Analytics Essentials",
            "tag": "Fundamentals",
            "hours": "12-16 hrs/week",
            "summary": "Master spreadsheet analytics, VLOOKUP/XLOOKUP, Pivot Tables, logical formulas, and data hygiene.",
            "topics": [
                "Advanced formulas: INDEX-MATCH, XLOOKUP, SUMIFS, and COUNTIFS",
                "Dynamic pivot tables, slicers, and calculated fields",
                "Data validation rules, conditional formatting, and cleaning text anomalies",
                "Business KPIs: CAC, LTV, MRR, Gross Margins, and Churn Rate"
            ],
            "practical_task": "Create an automated financial and sales model in Excel with interactive scenario analysis.",
            "deliverable": "Multi-sheet financial model workbook with dynamic pivot charts."
        },
        {
            "phase": "Weeks 3–4: SQL Mastery for Business Intelligence",
            "tag": "Core Skills",
            "hours": "16-20 hrs/week",
            "summary": "Write complex SQL queries, multi-table joins, subqueries, and date/time aggregations.",
            "topics": [
                "INNER, LEFT, RIGHT, and FULL OUTER joins across multi-entity schemas",
                "Grouping, aggregations, HAVING clauses, and ROLLUP operations",
                "Date formatting, month-over-month (MoM) growth calculations",
                "Data extraction and transformation directly from operational databases"
            ],
            "practical_task": "Write SQL queries that extract monthly customer retention, churn cohorts, and revenue leakage.",
            "deliverable": "SQL script suite ready for production analytics and reporting."
        },
        {
            "phase": "Weeks 5–6: Data Visualization & BI Tools (Tableau / Power BI)",
            "tag": "Intermediate Concepts",
            "hours": "16-20 hrs/week",
            "summary": "Build high-impact visual reports, understand dashboard UX principles, and calculate DAX measures.",
            "topics": [
                "Principles of visual perception, color psychology, and chart selection",
                "Power BI / Tableau data modeling, star schemas, and relationship cardinalities",
                "DAX calculations: CALCULATE, ALL, FILTER, and time-intelligence functions",
                "Building executive dashboard summaries and drill-down pages"
            ],
            "practical_task": "Construct a multi-page Power BI / Tableau dashboard analyzing retail sales performance across regions.",
            "deliverable": "Interactive BI dashboard with drill-down filters and cross-highlighting."
        },
        {
            "phase": "Weeks 7–8: Python for Automated Reporting & Plotly",
            "tag": "Practical Exercises",
            "hours": "16-20 hrs/week",
            "summary": "Use Python and Pandas to automate repetitive reporting and build web-based interactive charts.",
            "topics": [
                "Automating CSV/Excel ingestion, cleaning, and export using Pandas",
                "Interactive charting with Plotly Express: Scatter, Sunburst, Bar, and Radar charts",
                "Exporting data summaries into automated HTML and PDF executive reports",
                "Connecting Python directly to cloud databases"
            ],
            "practical_task": "Build an automated Python script that reads weekly transaction logs and emails an executive summary PDF.",
            "deliverable": "Working Python automation script with automated PDF generation."
        },
        {
            "phase": "Weeks 9–10: End-to-End Business Analytics Capstone",
            "tag": "Projects",
            "hours": "18-22 hrs/week",
            "summary": "Deliver a complete business intelligence solution for a realistic industry scenario.",
            "topics": [
                "End-to-end pipeline: SQL database -> Python ETL -> Interactive Streamlit UI",
                "KPI tracking, user cohort analysis, and trend forecasting",
                "Writing executive summaries highlighting commercial action items",
                "Hosting and securing analytics dashboards"
            ],
            "practical_task": "Develop an interactive E-Commerce Intelligence Dashboard featuring customer segmentation and basket analysis.",
            "deliverable": "Live interactive Streamlit dashboard with downloadable CSV summaries."
        },
        {
            "phase": "Weeks 11–12: Portfolio Building & Analyst Interview Prep",
            "tag": "Portfolio & Interview",
            "hours": "14-18 hrs/week",
            "summary": "Assemble a visual portfolio, practice business case studies, and prepare for SQL technical interviews.",
            "topics": [
                "Creating a GitHub & Notion portfolio showcasing dashboards and SQL scripts",
                "Practicing live SQL whiteboard questions and business interpretation tasks",
                "Answering behavioral questions: how to handle conflicting stakeholder data requirements",
                "Resume tailoring for Data Analyst and Business Intelligence roles"
            ],
            "practical_task": "Record a 3-minute video presentation explaining the business ROI of your capstone dashboard.",
            "deliverable": "Live portfolio link, polished LinkedIn profile, and vetted resume."
        }
    ],

    "Software Developer": [
        {
            "phase": "Weeks 1–2: Advanced OOP & Low-Level Programming",
            "tag": "Fundamentals",
            "hours": "18-22 hrs/week",
            "summary": "Deepen mastery of C++, Java, or Python, memory management, pointers, and SOLID principles.",
            "topics": [
                "Memory allocation: Stack vs. Heap, pointers, references, and smart pointers",
                "Object-Oriented Design: Polymorphism, Encapsulation, Abstraction, and Inheritance",
                "SOLID software design principles and clean code conventions",
                "Version control mastery: Git branches, rebase, cherry-pick, and pull requests"
            ],
            "practical_task": "Build a custom memory allocator or generic data structures library in C++ / Java.",
            "deliverable": "Clean GitHub repository with comprehensive unit tests and automated CI workflows."
        },
        {
            "phase": "Weeks 3–4: Data Structures & Algorithmic Rigor",
            "tag": "Core Skills",
            "hours": "20-25 hrs/week",
            "summary": "Master fundamental data structures, asymptotic time/space complexities, and problem-solving patterns.",
            "topics": [
                "Arrays, Linked Lists, Stacks, Queues, and Hash Maps",
                "Binary Trees, Binary Search Trees (BST), AVL Trees, and Heaps (Priority Queues)",
                "Big-O asymptotic analysis and space-time optimization tradeoffs",
                "Two Pointers, Sliding Window, and Fast-Slow Pointer patterns"
            ],
            "practical_task": "Solve 50 curated LeetCode Medium problems covering trees, graphs, and two-pointer techniques.",
            "deliverable": "LeetCode solutions repository with documented complexity analyses."
        },
        {
            "phase": "Weeks 5–6: Advanced Algorithms & System Concepts",
            "tag": "Intermediate Concepts",
            "hours": "20-25 hrs/week",
            "summary": "Explore Graph algorithms, Dynamic Programming, concurrency, and operating system concepts.",
            "topics": [
                "Graph traversals (BFS, DFS), Topological Sort, Dijkstra, and Bellman-Ford",
                "Dynamic Programming: Memoization, Tabulation, and Knapsack variants",
                "Concurrency: Threads, locks, mutexes, semaphores, and race condition prevention",
                "Inter-process communication (IPC) and socket programming basics"
            ],
            "practical_task": "Build a multithreaded web crawler or HTTP server with thread pool connection management.",
            "deliverable": "Working multithreaded server code with load testing benchmark results."
        },
        {
            "phase": "Weeks 7–8: Database Architecture & Backend REST APIs",
            "tag": "Practical Exercises",
            "hours": "18-22 hrs/week",
            "summary": "Design relational schemas, index strategies, transaction ACID guarantees, and RESTful APIs.",
            "topics": [
                "Relational database design (3NF normalization, foreign keys, constraints)",
                "Database transactions, ACID properties, and isolation levels",
                "Building RESTful APIs with FastAPI, Express, or Spring Boot",
                "Authentication and authorization using JWT and password hashing (bcrypt)"
            ],
            "practical_task": "Create a secure, documented REST API for a banking or inventory platform with role-based access.",
            "deliverable": "Swagger / OpenAPI documented backend with unit test coverage."
        },
        {
            "phase": "Weeks 9–10: Distributed Systems & Full-Stack Capstone",
            "tag": "Projects",
            "hours": "20-25 hrs/week",
            "summary": "Engineer a production-ready software system with caching, message queues, and containerization.",
            "topics": [
                "Caching strategies using Redis (Cache-aside, Write-through)",
                "Asynchronous task queues using Celery or RabbitMQ",
                "Containerizing application services using Docker and Docker Compose",
                "Monitoring, structured logging, and health check endpoints"
            ],
            "practical_task": "Build a real-time collaborative task management system with instant notifications and persistent storage.",
            "deliverable": "Fully containerized application runnable with a single `docker compose up` command."
        },
        {
            "phase": "Weeks 11–12: System Design & Technical Interview Preparation",
            "tag": "Portfolio & Interview",
            "hours": "18-22 hrs/week",
            "summary": "Master system design interview principles, coding mock interviews, and resume preparation.",
            "topics": [
                "System design basics: Load balancers, CDNs, horizontal scaling, and database sharding",
                "CAP theorem and eventual consistency vs strong consistency",
                "Mock algorithmic coding interviews under strict 45-minute constraints",
                "Resume engineering: Highlighting software performance metrics and technical stack"
            ],
            "practical_task": "Draft a complete system design document for a high-scale service like TinyURL or Pastebin.",
            "deliverable": "Architecture diagram, design whitepaper, and polished software engineering resume."
        }
    ],

    "Web Developer": [
        {
            "phase": "Weeks 1–2: Modern Semantic HTML5, CSS3 & Responsive Design",
            "tag": "Fundamentals",
            "hours": "14-18 hrs/week",
            "summary": "Master modern HTML5 semantics, CSS Flexbox, CSS Grid, custom properties, and responsive media queries.",
            "topics": [
                "Semantic HTML5 tags, accessibility (a11y), and SEO best practices",
                "Deep dive into CSS Flexbox and CSS Grid layout algorithms",
                "CSS variables, fluid typography (clamp), and CSS animations/transitions",
                "Mobile-first responsive design principles across mobile, tablet, and desktop"
            ],
            "practical_task": "Code a pixel-perfect, responsive marketing landing page with dark/light mode toggle from a Figma design.",
            "deliverable": "Hosted responsive website on GitHub Pages / Vercel with zero CSS frameworks."
        },
        {
            "phase": "Weeks 3–4: Modern JavaScript (ES6+) & DOM Manipulation",
            "tag": "Core Skills",
            "hours": "18-22 hrs/week",
            "summary": "Master JavaScript fundamentals, asynchronous programming, event loop, and DOM manipulation.",
            "topics": [
                "ES6+ features: Arrow functions, destructuring, spread/rest, template literals",
                "Asynchronous JS: Promises, async/await, and Fetch API",
                "Event bubbling, event delegation, and DOM manipulation",
                "Browser storage: LocalStorage, SessionStorage, and Cookies"
            ],
            "practical_task": "Build an interactive Weather Dashboard fetching data from a live REST API with dynamic city search.",
            "deliverable": "Interactive vanilla JavaScript application with debounce search and offline caching."
        },
        {
            "phase": "Weeks 5–6: Frontend Frameworks (React / Vue)",
            "tag": "Intermediate Concepts",
            "hours": "18-22 hrs/week",
            "summary": "Learn component-driven UI architecture, state management, hooks, and routing.",
            "topics": [
                "React JSX, components, props, and conditional rendering",
                "React Hooks: useState, useEffect, useRef, useMemo, and custom hooks",
                "Client-side routing with React Router",
                "Global state management with Context API or Zustand"
            ],
            "practical_task": "Build a responsive E-Commerce application with product filters, shopping cart, and persistent checkout state.",
            "deliverable": "Modern React web application deployed on Vercel with automated continuous deployment."
        },
        {
            "phase": "Weeks 7–8: Backend Web Development with Node.js / Python",
            "tag": "Practical Exercises",
            "hours": "18-22 hrs/week",
            "summary": "Build server-side backends, RESTful endpoints, database integration, and authentication.",
            "topics": [
                "Node.js & Express.js or Python FastAPI server architecture",
                "Middleware patterns, request validation, and error handling",
                "Connecting to MongoDB / PostgreSQL databases using ORMs",
                "JWT authentication, password hashing, and CORS policies"
            ],
            "practical_task": "Create a complete authentication backend with registration, login, JWT cookies, and protected user profiles.",
            "deliverable": "Production-ready backend API with Postman test collection."
        },
        {
            "phase": "Weeks 9–10: Full-Stack Web Application Capstone",
            "tag": "Projects",
            "hours": "20-25 hrs/week",
            "summary": "Connect modern frontend, robust backend, live database, and cloud deployment into a cohesive web app.",
            "topics": [
                "Full-stack architecture integration: React frontend + REST API + Database",
                "Real-time features using WebSockets or Server-Sent Events",
                "File uploads, cloud storage (AWS S3 or Cloudinary), and image optimization",
                "Web performance auditing: Lighthouse scores, lazy loading, and asset minification"
            ],
            "practical_task": "Build a Full-Stack Collaborative Project Management Kanban Board (Trello clone) with drag-and-drop.",
            "deliverable": "Live full-stack web application with GitHub repository, video demo, and Lighthouse score > 90."
        },
        {
            "phase": "Weeks 11–12: Performance, Portfolio & Web Dev Interview Prep",
            "tag": "Portfolio & Interview",
            "hours": "15-18 hrs/week",
            "summary": "Polish developer portfolio, master frontend interview questions, and prepare technical demonstrations.",
            "topics": [
                "JavaScript fundamentals interview questions: Closures, prototypes, hoisting, and this keyword",
                "Building an interactive, 3D/animated developer portfolio website",
                "Web security basics: XSS, CSRF, and SQL Injection prevention",
                "Resume tailoring and live coding challenge strategies"
            ],
            "practical_task": "Publish your personal interactive developer portfolio highlighting your top 3 live web projects.",
            "deliverable": "Live developer portfolio website with custom domain and verified GitHub activity."
        }
    ],

    "Cybersecurity Analyst": [
        {
            "phase": "Weeks 1–2: Networking Fundamentals & Linux Administration",
            "tag": "Fundamentals",
            "hours": "16-20 hrs/week",
            "summary": "Master the OSI model, TCP/IP stack, subnetting, DNS, and fundamental Linux terminal operations.",
            "topics": [
                "OSI 7-layer model and TCP/IP protocol suite deep dive",
                "IPv4/IPv6 addressing, subnet masking (CIDR), and routing basics",
                "Linux command line: File permissions (chmod/chown), process management, and grep",
                "SSH, bash scripting, and configuring firewall rules (iptables / ufw)"
            ],
            "practical_task": "Configure an isolated virtual network in VirtualBox with custom subnets and secure Linux bastion host.",
            "deliverable": "Network topology diagram and bash configuration script."
        },
        {
            "phase": "Weeks 3–4: Network Traffic Analysis & Wireshark",
            "tag": "Core Skills",
            "hours": "18-22 hrs/week",
            "summary": "Capture and dissect live packet captures (PCAP), identify anomalies, and analyze network protocols.",
            "topics": [
                "Packet capture with Wireshark and tcpdump",
                "Analyzing TCP three-way handshakes, TLS handshakes, and DNS requests",
                "Detecting port scans, ARP spoofing, and SYN flood attacks in PCAP files",
                "Network mapping and reconnaissance with Nmap scripts"
            ],
            "practical_task": "Analyze 5 mystery PCAP files to identify malicious exfiltration and port scanning activities.",
            "deliverable": "Detailed incident analysis report outlining timestamps, attacker IPs, and mitigation actions."
        },
        {
            "phase": "Weeks 5–6: Web Application Security & OWASP Top 10",
            "tag": "Intermediate Concepts",
            "hours": "18-22 hrs/week",
            "summary": "Understand application attack vectors, SQL injection, Cross-Site Scripting (XSS), and remediation.",
            "topics": [
                "OWASP Top 10 vulnerabilities explained with live exploits",
                "SQL Injection (SQLi): Union-based, Error-based, and Blind attacks",
                "Cross-Site Scripting (XSS): Stored, Reflected, and DOM-based attacks",
                "Using Burp Suite Community for intercepting HTTP proxy traffic"
            ],
            "practical_task": "Complete PortSwigger Web Security Academy practitioner labs covering SQLi and XSS.",
            "deliverable": "Lab completion certificates and vulnerability writeups."
        },
        {
            "phase": "Weeks 7–8: Security Operations (SOC) & SIEM Tools",
            "tag": "Practical Exercises",
            "hours": "18-22 hrs/week",
            "summary": "Learn security incident monitoring, log analysis, threat intelligence, and SIEM platforms.",
            "topics": [
                "Introduction to SIEM architecture (Splunk, Elastic SIEM)",
                "Parsing Windows Event Logs and Linux /var/log/syslog for suspicious behaviors",
                "Creating correlation rules to detect brute-force login attempts",
                "MITRE ATT&CK framework mapping for cyber kill-chains"
            ],
            "practical_task": "Set up a free Splunk or Elastic instance, ingest Apache/SSH logs, and build an alert dashboard.",
            "deliverable": "Configured SIEM dashboard detecting automated brute-force attacks in real time."
        },
        {
            "phase": "Weeks 9–10: Defensive & Offensive Security Capstone",
            "tag": "Projects",
            "hours": "20-25 hrs/week",
            "summary": "Build automated security tooling and complete realistic vulnerable machine assessments.",
            "topics": [
                "Developing automated vulnerability assessment tools in Python",
                "Scapy scripting for custom packet generation and detection",
                "Vulnerability assessment reporting with remediation recommendations",
                "Hardening server operating systems and SSH configurations"
            ],
            "practical_task": "Develop a lightweight automated Vulnerability Scanner in Python that audits open ports and headers.",
            "deliverable": "Working Python security scanner with automated PDF report generation."
        },
        {
            "phase": "Weeks 11–12: Certifications, Portfolio & Interview Prep",
            "tag": "Portfolio & Interview",
            "hours": "15-18 hrs/week",
            "summary": "Prepare for entry-level security certifications (CompTIA Security+, eJPT), writeups, and interview drills.",
            "topics": [
                "Review of CompTIA Security+ domains and core concepts",
                "Publishing technical vulnerability writeups on GitHub and TryHackMe profile",
                "Behavioral and scenario-based SOC analyst interview questions",
                "Formatting a security-focused CV emphasizing hands-on labs and CTFs"
            ],
            "practical_task": "Reach top 10% ranking on TryHackMe or solve 15 rooms and document solutions.",
            "deliverable": "Public cybersecurity writeup portfolio and verified TryHackMe / HackTheBox badges."
        }
    ],

    "Cloud Engineer": [
        {
            "phase": "Weeks 1–2: Operating Systems, Linux & Networking Fundamentals",
            "tag": "Fundamentals",
            "hours": "16-20 hrs/week",
            "summary": "Master core Linux systems, permissions, shell scripting, DNS, VPC concepts, and networking.",
            "topics": [
                "Linux system administration: users, groups, systemd services, and cron jobs",
                "Bash scripting for automated system maintenance and backups",
                "Networking: DNS records, NAT gateways, public vs private subnets, and routing tables",
                "Public key cryptography: SSH keys and SSL/TLS certificates"
            ],
            "practical_task": "Write an automated Bash backup script that compresses database snapshots and uploads to cloud storage.",
            "deliverable": "Automated script repository with error logging and crontab scheduling."
        },
        {
            "phase": "Weeks 3–4: Core Cloud Architecture (AWS / GCP / Azure)",
            "tag": "Core Skills",
            "hours": "18-22 hrs/week",
            "summary": "Explore core cloud compute, storage, virtual private clouds, and Identity and Access Management (IAM).",
            "topics": [
                "Virtual machines: EC2 / Compute Engine configuration and security groups",
                "Cloud storage: Object storage (S3), block storage (EBS), and lifecycle policies",
                "Virtual Private Cloud (VPC) peering, subnets, and internet gateways",
                "IAM: Users, roles, policies, least-privilege principles, and MFA"
            ],
            "practical_task": "Deploy a multi-tier web application inside a custom VPC with public and private subnets.",
            "deliverable": "Documented cloud architecture diagram and live working EC2 instance."
        },
        {
            "phase": "Weeks 5–6: Containers & Dockerization",
            "tag": "Intermediate Concepts",
            "hours": "18-22 hrs/week",
            "summary": "Master containerization concepts, Dockerfiles, multi-stage builds, and container networking.",
            "topics": [
                "Container vs Virtual Machine architecture tradeoffs",
                "Writing optimized, secure Dockerfiles with multi-stage builds",
                "Docker networking, volumes for persistent storage, and environment variables",
                "Multi-container orchestration using Docker Compose"
            ],
            "practical_task": "Dockerize a full-stack Python/Node web application with PostgreSQL and Nginx reverse proxy.",
            "deliverable": "Production-ready Docker Compose stack running with one command."
        },
        {
            "phase": "Weeks 7–8: Infrastructure as Code (Terraform) & CI/CD",
            "tag": "Practical Exercises",
            "hours": "18-22 hrs/week",
            "summary": "Automate cloud provisioning with Terraform and build automated continuous delivery pipelines.",
            "topics": [
                "Infrastructure as Code (IaC) principles, state management, and Terraform HCL",
                "Declaring VPCs, compute instances, and storage buckets declaratively",
                "Continuous Integration & Continuous Delivery (CI/CD) with GitHub Actions",
                "Automated testing, linting, and container builds on git push"
            ],
            "practical_task": "Write Terraform scripts to automatically provision a complete cloud web environment from scratch.",
            "deliverable": "Tested Terraform repository with automated GitHub Actions CI/CD workflow."
        },
        {
            "phase": "Weeks 9–10: Kubernetes & Cloud Capstone Project",
            "tag": "Projects",
            "hours": "20-25 hrs/week",
            "summary": "Learn Kubernetes container orchestration and build an enterprise-grade cloud native deployment.",
            "topics": [
                "Kubernetes architecture: Control Plane, Nodes, Pods, Deployments, and Services",
                "ConfigMaps, Secrets, Ingress controllers, and Horizontal Pod Autoscalers (HPA)",
                "Deploying containerized microservices to a local cluster (Minikube / k3s)",
                "Monitoring cloud resources with Prometheus and Grafana metrics"
            ],
            "practical_task": "Deploy an autoscaling microservices application on Kubernetes with automated ingress and monitoring.",
            "deliverable": "Working Kubernetes manifest suite with Grafana dashboard screenshots."
        },
        {
            "phase": "Weeks 11–12: Cloud Certifications, Portfolio & Interviews",
            "tag": "Portfolio & Interview",
            "hours": "15-18 hrs/week",
            "summary": "Prepare for AWS Certified Cloud Practitioner / Solutions Architect Associate, portfolio, and viva.",
            "topics": [
                "Well-Architected Framework: Reliability, security, cost optimization, performance",
                "Drafting technical case studies explaining cost reduction and uptime improvements",
                "Mock technical interviews for Cloud & DevOps roles",
                "Finalizing resume and LinkedIn profile showcasing Terraform and Cloud projects"
            ],
            "practical_task": "Complete a full AWS Solutions Architect practice exam and publish an architecture case study.",
            "deliverable": "High-impact cloud portfolio repository with architecture diagrams and IaC code."
        }
    ]
}


def get_roadmap_for_career(career_title):
    """
    Returns the tailored 12-week roadmap for the requested career domain.
    Falls back to Software Developer if the domain is not explicitly defined.
    """
    return ROADMAP_TEMPLATES.get(career_title, ROADMAP_TEMPLATES["Software Developer"])
