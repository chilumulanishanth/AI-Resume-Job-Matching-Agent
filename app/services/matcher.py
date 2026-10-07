import re
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

SKILL_ALIASES = {
    "python": ["python"],
    "sql": ["sql", "mysql", "postgresql", "postgres"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "django": ["django"],
    "rest api": ["rest api", "restful api", "rest"],
    "git": ["git", "github"],
    "docker": ["docker", "containerization", "containers"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services", "ec2", "s3", "rds"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "pyspark": ["pyspark", "spark"],
    "machine learning": ["machine learning", "ml"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "llm": ["llm", "large language model", "generative ai"],
    "rag": ["rag", "retrieval augmented generation", "retrieval-augmented generation"],
    "openai api": ["openai api", "openai"],
    "postgresql": ["postgresql", "postgres"],
    "pytest": ["pytest"],
    "selenium": ["selenium"],
    "playwright": ["playwright"],
    "linux": ["linux"],
    "ci/cd": ["ci/cd", "cicd", "continuous integration", "continuous delivery"],
}

def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())

def extract_skills(text: str) -> List[str]:
    t = _normalise(text)
    found = []
    for canonical, aliases in SKILL_ALIASES.items():
        if any(re.search(r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)", t) for alias in aliases):
            found.append(canonical)
    return sorted(found)

def retrieve_relevant_resume_sentences(resume_text: str, job_description: str, top_k: int = 5):
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", resume_text) if len(s.strip()) > 15]
    if not sentences:
        return []
    corpus = sentences + [job_description]
    matrix = TfidfVectorizer(stop_words="english").fit_transform(corpus)
    scores = cosine_similarity(matrix[-1], matrix[:-1]).flatten()
    ranked = sorted(zip(sentences, scores), key=lambda x: x[1], reverse=True)
    return [{"text": s, "score": round(float(score), 4)} for s, score in ranked[:top_k]]

def match_resume_to_job(resume_text: str, job_description: str) -> Dict:
    resume_skills = set(extract_skills(resume_text))
    job_skills = set(extract_skills(job_description))
    matched = sorted(resume_skills & job_skills)
    missing = sorted(job_skills - resume_skills)

    skill_score = (len(matched) / len(job_skills) * 100) if job_skills else 0
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform([resume_text, job_description])
    similarity = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0]) * 100

    overall = round((skill_score * 0.7) + (similarity * 0.3), 2)

    return {
        "overall_match_score": overall,
        "skill_match_score": round(skill_score, 2),
        "text_similarity_score": round(similarity, 2),
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_skills_detected": sorted(resume_skills),
        "job_skills_detected": sorted(job_skills),
        "retrieved_resume_evidence": retrieve_relevant_resume_sentences(resume_text, job_description),
    }
