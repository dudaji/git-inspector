# Cloud Functions for Git Inspector

## Installation

0. Install gcloud-cli
1. Install poetry
2. Run poetry virtual environment

   ```bash
   poetry shell
   ```

3. Install dependencies

```bash
poetry install
```

## How To Write

- Write cloud functions to main.py

## How To Test Locally

1. Run cloud function locally

   ```bash
   functions-framework-python --target <cloud-function-name>
   ```

2. Go to localhost:8080

## How To Deploy

```bash
gcloud functions deploy <cloud-function-name> \
  --gen2 \
  --region=<region> \
  --runtime=python39 \
  --source=. \
  --entry-point=<cloud-function-entrypoint-function-name> \
  --trigger-http
```
