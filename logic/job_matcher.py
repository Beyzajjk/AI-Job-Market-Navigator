from logic.job_market_engine import (
    load_jobs,
    split_skills
)


def match_jobs(user_skills, limit=5):
    df = load_jobs()

    user_set = set(
        skill.lower()
        for skill in user_skills
    )

    matches = []

    for _, row in df.iterrows():
        job_skills = split_skills(
            row["job_skills"]
        )

        if not job_skills:
            continue

        job_set = set(
            skill.lower()
            for skill in job_skills
        )

        common_skills = user_set.intersection(
            job_set
        )

        score = int(
            len(common_skills) / len(job_set) * 100
        )

        missing = list(
            job_set - user_set
        )

        matches.append({
            "title": row.get("job_title", "Unknown Role"),
            "company": row.get("company", "Unknown Company"),
            "location": row.get("job_location", "Unknown Location"),
            "score": score,
            "required_skills": job_skills,
            "missing_skills": missing,
            "summary": row.get("job_summary", "")
        })

    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return matches[:limit]