import hashlib
import json
from typing import Optional, Dict
from firebase_functions import https_fn
from functions.analyzer.full_analyzer import analyze_full_steps, analyze_with_mock
import os

from dotenv import load_dotenv
from firebase_functions import https_fn

from functions.analyzer.model import Scores, DetailedScore
from functions.firestore import check_cache, save_to_firestore
from functions.git import get_latest_commit_sha
from functions.analyzer.full_analyzer import FinalResponse, analyze_full_steps

load_dotenv()
os.environ["LANGCHAIN_PROJECT"] = "Git Analyzer"
os.environ["LANGCHAIN_TRACING_V2"] = "true"


def get_gemini_analysis_key(
    repo_url: str, branch: str, directory: Optional[str], commit_hash: str
) -> str:
    combined = f"{repo_url}{branch}{directory}{commit_hash}"
    hash_key = hashlib.md5(combined.encode("utf-8")).hexdigest()
    return hash_key


def calculate_scores(results: FinalResponse) -> Scores:
    filtered = {
        "aws": results.aws,
        "gcp": results.gcp,
        "azure": results.azure,
    }
    scores: Dict[str, DetailedScore] = {}

    costs = [p.instance.cost_per_hour for p in filtered.values()]
    cpus = [p.instance.cpu for p in filtered.values()]
    rams = [p.instance.ram for p in filtered.values()]
    carbon_footprints = [
        float(p.estimate.carbon_footprint.split(" ")[0]) for p in filtered.values()
    ]

    min_cost = min(costs)
    max_cost = max(costs)
    max_cpu = max(cpus)
    max_ram = max(rams)
    min_carbon = min(carbon_footprints)
    max_carbon = max(carbon_footprints)

    for name, provider in filtered.items():
        cost = provider.instance.cost_per_hour
        cpu = provider.instance.cpu
        ram = provider.instance.ram
        carbon_footprint = float(provider.estimate.carbon_footprint.split(" ")[0])
        has_gpu = provider.instance.gpu is not None

        cost_efficiency = (
            40 - ((cost - min_cost) / (max_cost - min_cost)) * 30
            if max_cost != min_cost
            else 40
        )
        cpu_score = (cpu / max_cpu) * 10 if max_cpu != 0 else 0
        ram_score = (ram / max_ram) * 10 if max_ram != 0 else 0
        gpu_score = 10 if has_gpu else 0
        performance = cpu_score + ram_score + gpu_score
        environmental_impact = (
            30 - ((carbon_footprint - min_carbon) / (max_carbon - min_carbon)) * 20
            if max_carbon != min_carbon
            else 30
        )
        total = cost_efficiency + performance + environmental_impact

        scores[name] = DetailedScore(
            cost_efficiency=cost_efficiency,
            performance=performance,
            environmental_impact=environmental_impact,
            total=total,
        )

    winner = max(scores, key=lambda key: scores[key].total)

    language_ratio = results.language_ratio
    total_bytes = sum(language_ratio.values())
    if total_bytes == 0:
        language_score = 0
    else:
        language_score = (
            sum(bytes_count * 0.1 for bytes_count in language_ratio.values())
            / total_bytes
        )

    return Scores(
        winner=winner,
        gcp=scores["gcp"],
        aws=scores["aws"],
        azure=scores["azure"],
        language=language_score,
    )


def analyze(request: https_fn.Request) -> dict:
    body = request.get_json(silent=True)
    print(body)

    repo_url = body.get("repoUrl")
    branch = body.get("branchName", "main")
    directory = body.get("directory", "")

    commit_hash = get_latest_commit_sha(repo_url, branch)
    hash_key = get_gemini_analysis_key(repo_url, branch, directory, commit_hash)

    if cache := check_cache(hash_key):
        print("Cache hit")
        return cache

    print("Analysis start")
    result = analyze_full_steps(repo_url, branch, directory)
    scores = calculate_scores(result)
    result_dict = json.loads(result.json())
    save_to_firestore(hash_key, repo_url, branch, directory, result_dict, scores)

    print("Analyzed Results", result)
    return result_dict
