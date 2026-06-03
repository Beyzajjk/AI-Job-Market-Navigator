from logic.job_market_engine import (
    get_top_market_skills
)


def analyze_skill_gap(
    user_skills
):

    top_skills = (
        get_top_market_skills(
            limit=10
        )
    )

    market_skills = list(
        top_skills.index
    )

    missing_skills = [

        skill

        for skill in market_skills

        if skill not in user_skills
    ]

    return missing_skills