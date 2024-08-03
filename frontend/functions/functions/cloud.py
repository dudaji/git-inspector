from firebase_functions import https_fn
from functions.analyzer.full_analyzer import analyze_full_steps
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGCHAIN_PROJECT"] = "Git Analyzer"
os.environ["LANGCHAIN_TRACING_V2"] = "true"


def analyze(request: https_fn.Request):
    body = request.get_json(silent=True)
    result = analyze_full_steps(
        body["repoUrl"], body.get("branchName", "main"), body.get("directory", "")
    )
    return result.json()
