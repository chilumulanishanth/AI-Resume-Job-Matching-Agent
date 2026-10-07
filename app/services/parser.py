from io import BytesIO
from pathlib import Path
import re

def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def extract_text(filename: str, content: bytes) -> str:
    ext = Path(filename).suffix.lower()

    if ext in {".txt", ".md"}:
        return _clean(content.decode("utf-8", errors="ignore"))

    if ext == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(BytesIO(content))
            return _clean("\n".join(page.extract_text() or "" for page in reader.pages))
        except Exception as exc:
            raise ValueError(f"Could not read PDF: {exc}")

    if ext == ".docx":
        try:
            from docx import Document
            doc = Document(BytesIO(content))
            return _clean("\n".join(p.text for p in doc.paragraphs))
        except Exception as exc:
            raise ValueError(f"Could not read DOCX: {exc}")

    raise ValueError("Unsupported file type. Use PDF, DOCX, TXT or MD.")
