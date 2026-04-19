import streamlit as st
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Resume Analyzer", layout="wide")

st.title("📄 Resume Analyzer + Job Recommendation")

# ---------------------------
# EXTRACT TEXT
# ---------------------------
def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.lower()

# ---------------------------
# CLEAN TEXT
# ---------------------------
def clean_text(text):
    replacements = {
        "eda": "exploratory data analysis",
        "ml": "machine learning",
        "dl": "deep learning",
        "js": "javascript",
        "np": "numpy",
        "pd": "pandas"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text

# ---------------------------
# IDEAL RESUMES
# ---------------------------
IDEAL_RESUMES = {
    "Data Analyst": """
    data analyst python sql pandas numpy excel power bi tableau
    data cleaning exploratory data analysis statistics visualization
    dashboard business insights reporting
    """,

    "ML Engineer": """
    machine learning deep learning python tensorflow pytorch
    model training evaluation feature engineering scikit-learn
    neural networks deployment
    """,

    "Backend Developer": """
    python django flask api development database sql backend
    rest api authentication system design
    """,

    "Frontend Developer": """
    html css javascript react frontend web development
    responsive design ui ux
    """
}

# ---------------------------
# SKILLS LIST
# ---------------------------
SKILLS = [
    "python","java","c++","sql","excel","pandas","numpy",
    "machine learning","deep learning","html","css","javascript",
    "react","django","flask","power bi","tableau"
]

def extract_skills(text):
    return [skill for skill in SKILLS if skill in text]

# ---------------------------
# FINAL SCORING FUNCTION
# ---------------------------
def calculate_score(text):

    text = clean_text(text)

    best_score = 0
    best_role = ""

    for role, ideal in IDEAL_RESUMES.items():
        vect = TfidfVectorizer(stop_words="english")
        tfidf = vect.fit_transform([ideal, text])

        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

        if sim > best_score:
            best_score = sim
            best_role = role

    similarity_score = best_score * 10

    # Skill Score
    skills_found = extract_skills(text)
    skill_score = min(len(skills_found) * 0.9, 10)

    # Project Score
    project_keywords = [
        "project", "developed", "built", "created",
        "prediction", "analysis", "model", "deployment"
    ]

    project_count = sum(text.count(word) for word in project_keywords)
    project_score = min(project_count * 1.2, 10)

    # Base Score
    base_score = 2.5

    # Final Score
    final_score = (
        0.4 * similarity_score +
        0.35 * skill_score +
        0.25 * project_score +
        base_score
    )

    return best_role, round(min(final_score, 10), 2), skills_found

# ---------------------------
# JOB LINKS
# ---------------------------
def job_links(role):
    query = role.replace(" ", "%20")
    linkedin = f"https://www.linkedin.com/jobs/search/?keywords={query}"
    naukri = f"https://www.naukri.com/{query}-jobs"
    return linkedin, naukri

# ---------------------------
# UI
# ---------------------------
file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if file:

    text = extract_text(file)

    if st.button("🚀 Analyze Resume"):

        role, score, skills = calculate_score(text)

        # 🔥 ADJUSTED SCORE (DEDUCT 1)
        adjusted_score = max(score - 1, 0)

        # ATS SCORE
        st.subheader("🎯 ATS Score")
        st.metric("Score", f"{adjusted_score}/10")
        st.progress(adjusted_score / 10)

        # ROLE
        st.subheader("💼 Best Role Match")

        if role:
            st.success(role)
        else:
            st.warning("No strong role detected")

        # SKILLS
        st.subheader("🧠 Extracted Skills")

        if skills:
            st.write(", ".join(skills))
        else:
            st.warning("No skills detected")

        # JOB LINKS
        if role:
            st.subheader("🔗 Job Opportunities")

            linkedin, naukri = job_links(role)

            st.markdown(f"[🔗 LinkedIn Jobs]({linkedin})")
            st.markdown(f"[🔗 Naukri Jobs]({naukri})")

        # MISSING SKILLS
        st.subheader("📉 Missing Skills")

        if role and role in IDEAL_RESUMES:

            required = IDEAL_RESUMES[role].split()
            missing = list(set(required) - set(skills))

            if missing:
                st.write("Skills you should improve:")
                st.write(", ".join(missing))
            else:
                st.success("You have most required skills! 🔥")

        else:
            st.warning("⚠️ Could not determine missing skills due to weak role match.")