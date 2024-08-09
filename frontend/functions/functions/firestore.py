import json
from typing import Optional, Union

from pydantic import BaseModel

import firebase_admin
from firebase_admin import firestore

from functions.analyzer.model import GeminiAnalysis, Scores
from functions.analyzer.full_analyzer import FinalResponse


def get_from_firestore(collection: str, key: str) -> Optional[dict]:
    db = None
    if firebase_admin._apps:
        db = firestore.client()
    else:
        raise SystemError("Firebase app is not initialized")

    analysis_ref = db.collection(collection).document(key)
    doc = analysis_ref.get()

    if doc.exists:
        return doc.to_dict()

    return None


def check_cache(gemini_analysis_key: str) -> Optional[dict]:
    db = None
    if firebase_admin._apps:
        db = firestore.client()
    else:
        raise SystemError("Firebase app is not initialized")

    analysis_ref = db.collection("gemini_analysis").document(gemini_analysis_key)
    doc = analysis_ref.get()

    if doc.exists:
        res = doc.to_dict()
        return res.get("result") if res else None

    return None


def save_gemini_analysis(
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


def save_to_firestore(collection: str, key: str, data: Union[dict, BaseModel]) -> None:
    db = None
    if firebase_admin._apps:
        db = firestore.client()
    else:
        raise SystemError("Firebase app is not initialized")

    data_dict = data if isinstance(data, dict) else {}
    if isinstance(data, BaseModel):
        data_dict = json.loads(data.model_dump_json())

    doc_ref = db.collection(collection).document(key)
    if data_dict:
        doc_ref.set(data_dict)
