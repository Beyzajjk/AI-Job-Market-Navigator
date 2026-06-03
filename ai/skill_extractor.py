TECH_SKILLS = [
    "Python", "SQL", "R", "Java", "Scala", "C++",
    "Excel", "Power BI", "Tableau",
    "Pandas", "NumPy", "Scikit-learn",
    "Machine Learning", "Deep Learning",
    "TensorFlow", "PyTorch", "Keras",
    "Statistics", "Data Analysis", "Data Visualization",
    "Docker", "Kubernetes", "Git",
    "AWS", "Azure", "GCP",
    "Spark", "Hadoop", "ETL",
    "NLP", "Computer Vision",
    "MLOps", "FastAPI", "Flask"
]


def extract_skills(text):
    detected_skills = []
    text_lower = text.lower()

    for skill in TECH_SKILLS:
        if skill.lower() in text_lower:
            detected_skills.append(skill)

    return list(set(detected_skills))