from typing import List
from collectors.models.cloud_cost import CloudCost
from google.cloud import firestore
import os
from datetime import datetime
import pytz
import pandas as pd


os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "../../secrets/firebase-svc-account-key.json"


def read_csv_to_cloudcost(file_path: str) -> List[CloudCost]:
    df = pd.read_csv(file_path)
    cloud_costs = []
    for _, row in df.iterrows():
        cloud_cost = CloudCost(
            vendor=row['vendor'],
            name=row['name'],
            region=row['region'],
            cpu=row['cpu'],
            ram=row['ram'],
            cost_per_hour=row['cost_per_hour'],
            extraction_date=row['extraction_date']
        )
        cloud_costs.append(cloud_cost)
    return cloud_costs


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
            new_data["last_updated"] = datetime.now(pytz.UTC).strftime("%Y-%m-%d")

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


def save_to_firestore_each(item: CloudCost):
    try:
        db = firestore.Client()
        print("Connected to Firestore.")
        collection_ref = db.collection("cloud_cost")
        count = 0
        update_count = 0

        doc_id = f"{item.vendor}_{item.region}_{item.name}"
        doc_ref = collection_ref.document(doc_id)
        doc = doc_ref.get()

        new_data = item.model_dump()
        new_data["last_updated"] = datetime.now(pytz.UTC).strftime("%Y-%m-%d")

        if doc.exists:
            existing_data = doc.to_dict()
            # Check if the existing data is different from the new data
            if existing_data != new_data:
                doc_ref.update(new_data)
                update_count += 1
        else:
            doc_ref.set(new_data)
            count += 1

        print(f"All data has been saved to Firestore. {item}")

    except Exception as e:
        print(f"Failed to save data to Firestore: {e}")


if __name__ == "__main__":
    csv_file_path = '../gcp_cloud_scraper/gcp_cloud_costs.csv'  # Your CSV file path
    cloud_costs = read_csv_to_cloudcost(csv_file_path)
    save_to_firestore(cloud_costs)