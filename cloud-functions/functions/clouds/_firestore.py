from typing import List
from model import CloudCost
from google.cloud import firestore
import os
from datetime import datetime

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "../../secrets/firebase-svc-account-key.json"


def save_to_firestore(data: List[CloudCost]):
    try:
        db = firestore.Client()
        print("Connected to Firestore.")
        collection_ref = db.collection("cloud_cost")
        count = 0
        update_count = 0

        for item in data:
            doc_id = f"{item.vendor}_{item.region}_{item.name}"
            doc_ref = collection_ref.document(doc_id)
            doc = doc_ref.get()

            new_data = item.model_dump()
            new_data["last_updated"] = datetime.now(datetime.UTC).strftime(
                "%Y-%m-%d"
            )

            if doc.exists:
                existing_data = doc.to_dict()
                # Check if the existing data is different from the new data
                if existing_data != new_data:
                    doc_ref.update(new_data)
                    update_count += 1
            else:
                doc_ref.set(new_data)
                count += 1

        print(
            f"All data has been saved to Firestore. Total new documents: {count}, Total updated documents: {update_count}"
        )

    except Exception as e:
        print(f"Failed to save data to Firestore: {e}")
