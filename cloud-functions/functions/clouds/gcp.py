from google.oauth2 import service_account
from googleapiclient.discovery import build
from model import CloudCost
from typing import List
import os
import re
import json
import csv


def fetch_and_save_gcp_prices():
    if os.path.exists("gcp_skus.json"):
        print("gcp_skus.json already exists. Skipping download.")
        return
    # Update with the path to your service account JSON file
    SERVICE_ACCOUNT_FILE = "../../secrets/git-inspector-dudaji-gcp.json"

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    service = build("cloudbilling", "v1", credentials=credentials)

    all_skus = []
    request = service.services().skus().list(parent="services/6F81-5844-456A")

    while request is not None:
        response = request.execute()
        all_skus.extend(response.get("skus", []))
        request = (
            service.services()
            .skus()
            .list_next(previous_request=request, previous_response=response)
        )

    with open("gcp_skus.json", "w") as json_file:
        json.dump(all_skus, json_file, indent=4)

    print(f"Data saved to gcp_skus.json with {len(all_skus)} items.")


def parse_gcp_prices_from_file():
    with open("gcp_skus.json", "r") as json_file:
        data = json.load(json_file)

    gcp_prices = []
    skipped_items = 0
    for sku in data:
        description = sku.get("description", "")
        category = sku.get("category", {})
        resource_group = category.get("resourceGroup", "")
        service_regions = sku.get("serviceRegions", ["global"])
        region = service_regions[0]
        pricing_info = sku.get("pricingInfo", [])

        if pricing_info:
            tiered_rates = pricing_info[0]["pricingExpression"].get(
                "tieredRates", []
            )
            if tiered_rates:
                price_info = tiered_rates[0]["unitPrice"]
                cost_per_hour = price_info.get("nanos", 0) / 1e9

                try:
                    cloud_cost = CloudCost(
                        vendor="GCP",
                        name=description,
                        region=region,
                        cost_per_hour=cost_per_hour,
                    )

                    if resource_group == "GPU":
                        cloud_cost.gpu = "Yes"

                    gcp_prices.append(cloud_cost)
                except ValueError as e:
                    skipped_items += 1
                    print(f"Skipping item due to missing fields: {e}")
            else:
                skipped_items += 1
                print(f"Skipping item due to empty tieredRates.")
        else:
            skipped_items += 1
            print(f"Skipping item due to missing pricing_info.")

    print(f"Skipped {skipped_items} items due to missing required fields.")
    return gcp_prices


def save_to_csv(data: List[CloudCost], filename: str):
    with open(filename, "w", newline="") as csvfile:
        fieldnames = [
            "vendor",
            "name",
            "region",
            "cost_per_hour",
            "cpu",
            "ram",
            "gpu",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for item in data:
            writer.writerow(item.model_dump())
    print(f"Data saved to {filename}")


def main():
    fetch_and_save_gcp_prices()
    gcp_prices = parse_gcp_prices_from_file()
    save_to_csv(gcp_prices, "gcp_parsed_prices.csv")
    for price in gcp_prices:
        print(price)


if __name__ == "__main__":
    main()
