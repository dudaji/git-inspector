import hashlib
from typing import Optional, Dict
from firebase_functions import https_fn
from functions.analyzer.gemini_analyzer import analyze_repo
from functions.analyzer.model import Scores
from functions.firestore import check_cache, save_to_firestore

from functions.git import get_latest_commit_sha


def get_gemini_analysis_key(
    repo_url: str, branch: str, directory: Optional[str], commit_hash: str
) -> str:
    combined = f"{repo_url}{branch}{directory}{commit_hash}"
    hash_key = hashlib.md5(combined.encode("utf-8")).hexdigest()
    return hash_key


def calculate_scores(result) -> Scores:
    return None


def calculate_languages(result) -> Dict[str, float]:
    return None


def analyze(request: https_fn.Request):
    body = request.get_json(silent=True)
    print(body)

    repo_url = body.get("repoUrl")
    branch = body.get("branchName", "main")
    directory = body.get("directory")

    commit_hash = get_latest_commit_sha(repo_url, branch)
    hash_key = get_gemini_analysis_key(repo_url, branch, directory, commit_hash)

    if cache := check_cache(hash_key):
        return cache

    result = analyze_repo(repo_url, branch, directory)
    scores = calculate_scores(result)
    languages = calculate_languages(result)
    save_to_firestore(
        hash_key, repo_url, branch, directory, result, scores, languages
    )
    return result
