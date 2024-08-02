from typing import Optional, Dict
from firebase_admin import initialize_app, firestore
from functions.analyzer.model import GeminiAnalysis, Scores
from functions.analyzer.parser import Result

initialize_app()
db = firestore.client()


def check_cache(gemini_analysis_key: str) -> Optional[dict]:
    analysis_ref = db.collection("gemini_analysis").document(
        gemini_analysis_key
    )
    doc = analysis_ref.get()

    return doc.to_dict() if doc.exists else None


def save_to_firestore(
    key: str,
    repo_url: str,
    branch: str,
    directory: Optional[str],
    result: Result,
    scores: Scores,
    languages: Dict[str, float],
) -> None:
    if not result:
        raise SystemError("Gemini cannot generate result")

    doc_ref = db.collection("gemini_analysis").document(key)
    analysis = GeminiAnalysis(
        repo_url=repo_url,
        branch=branch,
        directory=directory,
        result=result,
        scores=scores,
        languages=languages,
    )
    doc_ref.set(analysis.to_dict())
