# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

import json
from firebase_functions import https_fn

from functions.cloud import get_cache, repo_analyzer, analyze


@https_fn.on_request(timeout_sec=300)
def analyzer(req: https_fn.Request) -> https_fn.Response:
    if req.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}
    result = analyze(req)
    return https_fn.Response(result, headers=headers, status=200)
    # return https_fn.Response("Hello world!")


@https_fn.on_request()
def analyze_step_by_step(req: https_fn.Request) -> https_fn.Response:
    if req.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)

    # Set CORS headers for the main request
    headers = {"Access-Control-Allow-Origin": "*"}

    uri_path = req.path
    method = req.method
    ret = {"error": "Unsupported api"}
    status = 400
    if method == "POST":
        if uri_path == "/cache":
            cache = get_cache(req)
            if cache is not None:
                ret = cache
                status = 200
        if uri_path == "/analyze-repo":  # step 1
            ret = repo_analyzer(req)
            status = 200

    return https_fn.Response(ret, headers=headers, status=status)
