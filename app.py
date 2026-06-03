import streamlit as st
import pandas as pd

from ai.skill_extractor import extract_skills
from logic.job_market_engine import get_top_market_skills
from logic.skill_gap_analyzer import analyze_skill_gap
from logic.job_matcher import match_jobs
from logic.roadmap_builder import build_roadmap


st.set_page_config(
    page_title="AI Job Market Navigator",
    page_icon="🚀",
    layout="wide"
)


st.markdown("""
<style>
.main {
    background-color: #f6f1fa;
}

.block-container {
    padding-top: 3rem;
    padding-left: 5rem;
    padding-right: 5rem;
}

.hero-title {
    font-size: 68px;
    font-weight: 300;
    line-height: 1.05;
    letter-spacing: -3px;
    color: #111111;
}

.hero-subtitle {
    font-size: 21px;
    color: #666666;
    max-width: 850px;
    margin-top: 20px;
    margin-bottom: 40px;
}

.card {
    background: rgba(255,255,255,0.82);
    border-radius: 28px;
    padding: 28px;
    margin-top: 22px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.05);
}

.card-title {
    font-size: 26px;
    font-weight: 600;
    margin-bottom: 18px;
    color: #111111;
}

.skill-pill {
    display: inline-block;
    background: #ffffff;
    border-radius: 999px;
    padding: 9px 16px;
    margin: 6px 6px 6px 0;
    font-size: 15px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
}

.warning-pill {
    display: inline-block;
    background: #fff3e8;
    border-radius: 999px;
    padding: 9px 16px;
    margin: 6px 6px 6px 0;
    font-size: 15px;
}

.job-card {
    background: white;
    border-radius: 22px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.05);
}

.job-title {
    font-size: 22px;
    font-weight: 600;
    color: #111111;
}

.small-text {
    color: #666666;
    font-size: 15px;
}

.stTextArea textarea {
    border-radius: 22px;
    padding: 20px;
    font-size: 16px;
}

.stButton button {
    background-color: #111111;
    color: white;
    border-radius: 999px;
    padding: 12px 30px;
    border: none;
    font-size: 16px;
}

.stButton button:hover {
    background-color: #333333;
    color: white;
}
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.markdown("## 🚀 AI Job Navigator")
    st.write("Real job-market based career analysis.")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Analyze Profile",
            "Market Insights",
            "Job Matches",
            "Roadmap"
        ]
    )

    st.divider()
    st.caption("Built with Streamlit, Pandas and real job posting data.")


if "user_skills" not in st.session_state:
    st.session_state.user_skills = []

if "missing_skills" not in st.session_state:
    st.session_state.missing_skills = []

if "job_matches" not in st.session_state:
    st.session_state.job_matches = []

if "roadmap" not in st.session_state:
    st.session_state.roadmap = []

if "top_market_skills" not in st.session_state:
    st.session_state.top_market_skills = pd.Series(dtype=int)

if "analyzed" not in st.session_state:
    st.session_state.analyzed = False


if page == "Dashboard":

    st.markdown("""
    <div class="hero-title">
    Navigate your career<br>
    with real job-market intelligence.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-subtitle">
    Analyze your current skills, compare them with real job postings,
    discover missing skills and build a personalized roadmap.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Detected Skills",
            len(st.session_state.user_skills)
        )

    with col2:
        st.metric(
            "Missing Skills",
            len(st.session_state.missing_skills)
        )

    with col3:
        if st.session_state.job_matches:
            best_score = st.session_state.job_matches[0]["score"]
        else:
            best_score = 0

        st.metric(
            "Best Match",
            f"{best_score}%"
        )

    if not st.session_state.analyzed:
        st.info("Go to Analyze Profile and run your first career analysis.")

    else:
        st.markdown("""
        <div class="card">
        <div class="card-title">Latest Analysis Summary</div>
        """, unsafe_allow_html=True)

        st.write("**Detected skills:**")
        for skill in st.session_state.user_skills:
            st.markdown(
                f"<span class='skill-pill'>{skill}</span>",
                unsafe_allow_html=True
            )

        st.write("**Top missing skills:**")
        for skill in st.session_state.missing_skills[:6]:
            st.markdown(
                f"<span class='warning-pill'>⚠️ {skill}</span>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)


elif page == "Analyze Profile":

    st.markdown("""
    <div class="hero-title">
    Tell the system<br>
    who you are.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-subtitle">
    Describe your education, skills, projects and career goals.
    The system will compare your profile with real job postings.
    </div>
    """, unsafe_allow_html=True)

    user_profile = st.text_area(
        "Your profile",
        placeholder="""
I graduated from Computer Engineering.
I know Python, SQL and Pandas.
I built a few machine learning projects.
I want to work in AI, Data Science or Data Analysis.
""",
        height=230
    )

    if st.button("Analyze My Career Fit"):

        user_skills = extract_skills(user_profile)
        top_market_skills = get_top_market_skills(limit=10)
        missing_skills = analyze_skill_gap(user_skills)
        job_matches = match_jobs(user_skills)
        roadmap = build_roadmap(missing_skills)

        st.session_state.user_skills = user_skills
        st.session_state.top_market_skills = top_market_skills
        st.session_state.missing_skills = missing_skills
        st.session_state.job_matches = job_matches
        st.session_state.roadmap = roadmap
        st.session_state.analyzed = True

        st.success("Analysis completed successfully.")

        st.markdown("""
        <div class="card">
        <div class="card-title">Detected Skills</div>
        """, unsafe_allow_html=True)

        if user_skills:
            for skill in user_skills:
                st.markdown(
                    f"<span class='skill-pill'>✅ {skill}</span>",
                    unsafe_allow_html=True
                )
        else:
            st.warning("No skills detected. Try writing more specific skills.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
        <div class="card-title">Missing Skills</div>
        """, unsafe_allow_html=True)

        for skill in missing_skills:
            st.markdown(
                f"<span class='warning-pill'>⚠️ {skill}</span>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)


elif page == "Market Insights":

    st.title("Market Insights")

    if not st.session_state.analyzed:
        st.info("Analyze your profile first.")

    else:
        top_market_skills = st.session_state.top_market_skills

        st.markdown("""
        <div class="card">
        <div class="card-title">Most Requested Skills</div>
        </div>
        """, unsafe_allow_html=True)

        chart_df = top_market_skills.reset_index()
        chart_df.columns = ["Skill", "Postings"]
        st.bar_chart(
            chart_df.set_index("Skill")
        )

        st.markdown("""
        <div class="card">
        <div class="card-title">Market Interpretation</div>
        """, unsafe_allow_html=True)

        most_requested = list(top_market_skills.index[:3])

        st.write(
            f"The most requested skills in the analyzed job postings are "
            f"**{', '.join(most_requested)}**. "
            f"Your roadmap should prioritize the missing skills that also appear frequently in the market."
        )

        st.markdown("</div>", unsafe_allow_html=True)


elif page == "Job Matches":

    st.title("Best Job Matches")

    if not st.session_state.analyzed:
        st.info("Analyze your profile first.")

    else:
        for job in st.session_state.job_matches:

            st.markdown("<div class='job-card'>", unsafe_allow_html=True)

            st.markdown(
                f"<div class='job-title'>{job['title']}</div>",
                unsafe_allow_html=True
            )

            st.write(f"**Match Score:** {job['score']}%")

            st.progress(job["score"] / 100)

            if "company" in job:
                st.write(f"**Company:** {job['company']}")

            if "location" in job:
                st.write(f"**Location:** {job['location']}")

            st.write("**Required Skills:**")
            for skill in job["required_skills"]:
                st.markdown(
                    f"<span class='skill-pill'>{skill}</span>",
                    unsafe_allow_html=True
                )

            st.write("**Missing Skills:**")
            for skill in job["missing_skills"]:
                st.markdown(
                    f"<span class='warning-pill'>⚠️ {skill}</span>",
                    unsafe_allow_html=True
                )

            if job.get("summary"):
                with st.expander("View job summary"):
                    st.write(job["summary"])

            st.markdown("</div>", unsafe_allow_html=True)


elif page == "Roadmap":

    st.title("Personalized Roadmap")

    if not st.session_state.analyzed:
        st.info("Analyze your profile first.")

    else:
        st.markdown("""
        <div class="card">
        <div class="card-title">Recommended Learning Path</div>
        """, unsafe_allow_html=True)

        for index, step in enumerate(st.session_state.roadmap, start=1):
            st.write(f"**Step {index}:** {step}")

        st.markdown("</div>", unsafe_allow_html=True)