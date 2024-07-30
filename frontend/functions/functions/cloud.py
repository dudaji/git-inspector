from firebase_functions import https_fn
from functions.analyzer.gemini_analyzer import analyze_repo


def analyze(request: https_fn.Request):
    body = request.get_json(silent=True)
    print(body)
    result = analyze_repo(
        body["repoUrl"], body.get("branchName", "main"), body.get("directory", "")
    )
    return result
