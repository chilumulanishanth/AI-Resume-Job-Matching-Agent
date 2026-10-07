# AI Resume & Job Matching Agent

An API-based AI recruitment assistant that compares a resume with a job description, detects relevant skills, retrieves the most relevant resume evidence, calculates a transparent match score, and optionally uses an LLM for qualitative analysis.

## Features

- PDF, DOCX, TXT and Markdown resume parsing
- Skill extraction with configurable skill aliases
- Deterministic skill-match score
- TF-IDF semantic-style text similarity
- Retrieval of the most relevant resume sentences
- Missing-skill analysis
- Optional OpenAI LLM analysis
- FastAPI REST endpoints
- Automated pytest coverage
- Docker support
- GitHub Actions CI

## Architecture

Client -> FastAPI -> Resume Parser -> Matching Engine -> Retrieval -> Optional LLM -> JSON Response

The deterministic matching layer works without an API key. The LLM layer is optional.

## Run locally

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`.

## API

### Health
`GET /health`

### Text matching
`POST /match`

Example:

```json
{
  "resume_text": "Python developer with FastAPI, SQL, Docker and Git experience.",
  "job_description": "We need a Python backend engineer with FastAPI, PostgreSQL, Docker and AWS."
}
```

### File matching
`POST /match-file`

Upload a PDF/DOCX/TXT/MD resume and provide `job_description` as form data.

## Docker

```bash
docker compose up --build
```

## Testing

```bash
pytest -q
```

## Responsible use

This project is a decision-support tool, not an autonomous hiring system. Match scores are heuristic signals and should not be used as the sole basis for employment decisions.
