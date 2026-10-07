from app.services.matcher import match_resume_to_job

def test_matcher_detects_shared_and_missing_skills():
    result = match_resume_to_job(
        "Python FastAPI SQL Git Docker",
        "Looking for Python, FastAPI, SQL and AWS experience."
    )
    assert "python" in result["matched_skills"]
    assert "aws" in result["missing_skills"]
    assert result["skill_match_score"] > 0
