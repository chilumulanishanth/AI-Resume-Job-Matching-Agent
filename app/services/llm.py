import os
from typing import Dict

def generate_ai_analysis(resume_text: str, job_description: str, result: Dict) -> Dict:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "provider": "local-fallback",
            "summary": "AI analysis is disabled because OPENAI_API_KEY is not configured.",
            "recommendations": [
                f"Highlight evidence for: {', '.join(result['matched_skills']) or 'your strongest relevant skills'}.",
                f"Address gaps: {', '.join(result['missing_skills']) or 'no major detected skill gaps'}.",
                "Add measurable outcomes and project evidence where possible."
            ]
        }

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        prompt = f"""You are a recruitment assistant. Analyze this resume against the job description.
Return concise JSON with keys: summary, strengths, gaps, recommendations.
Resume:
{resume_text[:12000]}

Job description:
{job_description[:12000]}

Deterministic matching result:
{result}
"""
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
            input=prompt
        )
        return {"provider": "openai", "analysis": response.output_text}
    except Exception as exc:
        return {
            "provider": "local-fallback",
            "summary": "LLM call failed, so deterministic matching results were returned.",
            "error": str(exc),
            "recommendations": ["Check OPENAI_API_KEY, model access, and network configuration."]
        }
