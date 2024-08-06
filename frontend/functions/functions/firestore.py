import json
from typing import Optional, Union

import firebase_admin
from firebase_admin import firestore

from functions.analyzer.model import GeminiAnalysis, Scores
from functions.analyzer.full_analyzer import FinalResponse


def check_cache(gemini_analysis_key: str) -> Optional[dict]:
    db = None
    if firebase_admin._apps:
        db = firestore.client()
    else:
        raise SystemError("Firebase app is not initialized")

    analysis_ref = db.collection("gemini_analysis").document(gemini_analysis_key)
    doc = analysis_ref.get()

    if doc.exists:
        return doc.to_dict().get("result")

    return None


def save_to_firestore(
    key: str,
    repo_url: str,
    branch: str,
    directory: Optional[str],
    result: Union[dict, FinalResponse],
    scores: Scores,
) -> None:
    result_dict = result
    if not result:
        raise SystemError("Gemini cannot generate result")

    if isinstance(result_dict, FinalResponse):
        result_dict = json.loads(result_dict.json())

    db = None
    if firebase_admin._apps:
        db = firestore.client()
    else:
        raise SystemError("Firebase app is not initialized")

    doc_ref = db.collection("gemini_analysis").document(key)
    analysis = GeminiAnalysis(
        repo_url=repo_url,
        branch=branch,
        directory=directory or "",
        result=result_dict,
        scores=scores,
    )
    print("Save Analysis")
    doc_ref.set(json.loads(analysis.model_dump_json()))
