import pandas as pd


POSTINGS_PATH = "data/job_postings.csv"
SKILLS_PATH = "data/job_skills.csv"
SUMMARY_PATH = "data/job_summary.csv"


def load_jobs():
    postings = pd.read_csv(POSTINGS_PATH)
    skills = pd.read_csv(SKILLS_PATH)
    summaries = pd.read_csv(SUMMARY_PATH)

    df = postings.merge(skills, on="job_link", how="left")
    df = df.merge(summaries, on="job_link", how="left")

    df["job_skills"] = df["job_skills"].fillna("")
    df["job_summary"] = df["job_summary"].fillna("")

    return df


def split_skills(skill_text):
    if not isinstance(skill_text, str):
        return []

    return [
        skill.strip()
        for skill in skill_text.split(",")
        if skill.strip()
    ]


def analyze_market():
    df = load_jobs()

    all_skills = []

    for skill_text in df["job_skills"]:
        all_skills.extend(split_skills(skill_text))

    skill_counts = pd.Series(all_skills).value_counts()

    return skill_counts


def get_top_market_skills(limit=10):
    skill_counts = analyze_market()
    return skill_counts.head(limit)