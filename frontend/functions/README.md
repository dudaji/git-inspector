# Cloud functions

## Run Locally

```bash
cd frontend/functions
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS="./firebase-svc-account-key.json"
firebase emulators:start --only functions
```
