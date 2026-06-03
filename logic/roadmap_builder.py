def build_roadmap(
    missing_skills
):

    roadmap = []

    for skill in missing_skills[:5]:

        roadmap.append(

            f"Learn {skill} "
            f"and build a project using it."
        )

    roadmap.append(

        "Upload clean projects "
        "to GitHub."
    )

    roadmap.append(

        "Apply to jobs where "
        "you match at least 60%."
    )

    return roadmap