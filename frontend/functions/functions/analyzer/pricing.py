from math import inf
from pathlib import Path
from google.cloud.firestore_v1.base_query import FieldFilter, Or, And
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from functions.analyzer.parser import Instance


def correct_instance_price(instance: Instance) -> Instance:
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-svc-account-key.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    ref = db.collection("cloud_cost")
    vendor_filter = FieldFilter("vendor", "==", instance.cloud_provider)
    name_filter = FieldFilter("name", "==", instance.name)
    cpu_filter = FieldFilter("cpu", "==", instance.cpu)
    ram_filter = FieldFilter("ram", "==", instance.ram)
    region_filter = FieldFilter("region", "==", instance.region)
    final_filter = And(
        filters=[vendor_filter, name_filter, cpu_filter, ram_filter, region_filter]
    )
    docs = list(ref.where(filter=final_filter).stream())
    if len(docs) == 1:
        return Instance(
            cloud_provider=instance.cloud_provider,
            storage=instance.storage,
            description=instance.description,
            **docs[0].to_dict(),
        )
    return instance


def get_cheapest_instance(instance: Instance) -> Instance:
    """
    Get the cheapest instance among candidate instances
    Args:
        instance (Instance): Instance estimated by gemini
    Returns:
        Instance: The cheapest instance
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            f"{Path(__file__).resolve().parent}/../../../firebase-svc-account-key.json"
        )
        app = firebase_admin.initialize_app(cred)
    db = firestore.client()
    ref = db.collection("cloud_cost")
    vendor_filter = FieldFilter("vendor", "==", instance.cloud_provider)
    name_filter = FieldFilter("name", "==", instance.name)
    cpu_filter = FieldFilter("cpu", "==", instance.cpu)
    ram_filter = FieldFilter("ram", "==", instance.ram)
    resource_filter = And(filters=[cpu_filter, ram_filter])
    instance_filter = Or(filters=[name_filter, resource_filter])
    final_filter = And(filters=[vendor_filter, instance_filter])
    docs = ref.where(filter=final_filter).stream()

    lowest_instance = {"cost_per_hour": float(inf)}
    for doc in docs:
        if lowest_instance["cost_per_hour"] > doc.to_dict()["cost_per_hour"]:
            lowest_instance = doc.to_dict()
    instance = Instance(
        cloud_provider=instance.cloud_provider,
        name=lowest_instance["name"],
        cpu=lowest_instance["cpu"],
        ram=lowest_instance["ram"],
        storage=instance.storage,
        gpu=lowest_instance["gpu"],
        region=lowest_instance["region"],
        cost_per_hour=lowest_instance["cost_per_hour"],
        description=instance.description,
    )
    return instance
