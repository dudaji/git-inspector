# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

import json
from firebase_functions import https_fn, options
import firebase_admin
from pathlib import Path
from firebase_admin import initialize_app, credentials

from functions.cloud import (
    environment_analyzer,
    get_best_instance,
    get_cache,
    repo_analyzer,
    analyze,
)

initialize_app()

if not firebase_admin._apps:
    cred = credentials.Certificate(
        f"{Path(__file__).resolve().parent}/../firebase-svc-account-key.json"
    )
    initialize_app(cred)


@https_fn.on_request(timeout_sec=300, memory=options.MemoryOption.GB_4)
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


@https_fn.on_request(timeout_sec=300, memory=options.MemoryOption.GB_4)
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
            else:
                ret = {"error": "No cache is found"}
                status = 404
        if (
            uri_path == "/analyze-repo"
        ):  # step 1: Get minimum instance spec per cloud provider
            ret = repo_analyzer(req)
            status = 200
        elif (
            uri_path == "/analyze-env"
        ):  # step 2: Calculate power consumption and carbon footprint
            ret = environment_analyzer(req)
            status = 200
        elif (
            uri_path == "/analyze-instance"
        ):  # step 3: Select the most eco friendly instance
            ret = get_best_instance(req)
            status = 200

    return https_fn.Response(json.dumps(ret), headers=headers, status=status)
