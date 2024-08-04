import hashlib
from firebase_functions import https_fn
import os
import json
from typing import Optional, Dict, Tuple
from firebase_functions import https_fn
from functions.analyzer.calculator import (
    estimate_environment,
    estimate_environment_mock,
)
from functions.analyzer.full_analyzer import (
    FinalResponse,
    analyze_full_steps,
    analyze_with_mock,
)

from dotenv import load_dotenv
from firebase_functions import https_fn

from functions.analyzer.instance_selector import select_best_instance
from functions.analyzer.model import Scores, DetailedScore
from functions.analyzer.parser import Instance, InstanceResult, RepoResult
from functions.firestore import check_cache, save_to_firestore
from functions.git import get_latest_commit_sha

from functions.analyzer.repo_analyzer import analyze_repo, analyze_repo_mock

from functions.analyzer.repo_analyzer import analyze_repo, analyze_repo_mock

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


def get_repo_info(
    repo_url: str, branch: str = "main", directory: str = ""
) -> Tuple[str, dict, str]:
    repo_path, commit_hash = get_latest_commit_sha(repo_url, branch)
    hash_key = get_gemini_analysis_key(repo_url, branch, directory, commit_hash)

    if cache := check_cache(hash_key):
        print("Cache hit")
        return None, cache, hash_key
    return repo_path, None, hash_key


def get_repo_body(request: https_fn.Request) -> Tuple[str, str, str]:
    body = request.get_json(silent=True)
    print(body)

    repo_url = body.get("repoUrl")
    branch = body.get("branchName", "main")
    directory = body.get("directory", "")

    return repo_url, branch, directory


def get_cache(request: https_fn.Request) -> dict | None:
    repo_url, branch, directory = get_repo_body(request)
    _, cache, _ = get_repo_info(repo_url, branch, directory)
    if cache:
        return cache
    return None


def analyze(request: https_fn.Request) -> dict:
    repo_url, branch, directory = get_repo_body(request)

    repo_path, cache, hash_key = get_repo_info(repo_url, branch, directory)
    if cache:
        return json.dumps(cache)

    print("Analysis start")
    result = analyze_full_steps(repo_path, directory)
    # result = analyze_with_mock(repo_path, directory)
    scores = calculate_scores(result)
    save_to_firestore(
        hash_key, repo_url, branch, directory, json.loads(result.json()), scores
    )

    print("Analyzed Results", result)
    return result.dict(by_alias=True)


def repo_analyzer(request: https_fn.Request) -> dict:
    body = request.get_json(silent=True)

    repo_url = body.get("repoUrl")
    branch = body.get("branchName", "main")
    directory = body.get("directory", "")
    repo_path, _ = get_latest_commit_sha(repo_url, branch)
    return analyze_repo_mock(repo_path, directory).dict(by_alias=True)


def environment_analyzer(request: https_fn.Request) -> dict:
    body = request.get_json(silent=True)

    aws_instance = Instance(**body.get("aws"))
    gcp_instance = Instance(**body.get("gcp"))
    azure_instance = Instance(**body.get("azure"))

    return estimate_environment_mock(aws_instance, gcp_instance, azure_instance).dict(
        by_alias=True
    )


def get_best_instance(request: https_fn.Request) -> dict:
    body = request.get_json(silent=True)

    repo_url = body.get("repoUrl")
    branch = body.get("branchName", "main")
    directory = body.get("directory", "")
    aws_instance = InstanceResult(**body.get("aws"))
    gcp_instance = InstanceResult(**body.get("gcp"))
    azure_instance = InstanceResult(**body.get("azure"))
    language_ratio = body.get("languageRatio")
    instance_results = [aws_instance, gcp_instance, azure_instance]
    best_instance = select_best_instance(instance_results)
    result = FinalResponse(
        aws=aws_instance,
        gcp=gcp_instance,
        azure=azure_instance,
        conclusion=best_instance,
        language_ratio=language_ratio,
    )
    _, _, hash_key = get_repo_info(repo_url, branch, directory)
    scores = calculate_scores(result)
    save_to_firestore(
        hash_key, repo_url, branch, directory, json.loads(result.json()), scores
    )
    return best_instance.dict(by_alias=True)
