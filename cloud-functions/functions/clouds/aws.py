import requests
import os
from datetime import datetime

# import csv
from typing import List
from model import CloudCost

# from google.cloud import firestore
from functions.clouds._firestore import save_to_firestore

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"
] = "../../secrets/firebase-svc-account-key.json"


def get_filtered_aws_prices(service_code: str, region: str) -> List[CloudCost]:
    url = f"https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/{service_code}/current/{region}/index.json"
    print(f"Requesting data from: {url}")
    response = requests.get(url)
    data = response.json()
    print(f"Data received from AWS Pricing API for region {region}")

    aws_prices = []
    extraction_date = datetime.now(datetime.UTC).strftime(
        "%Y-%m-%d"
    )  # 현재 날짜를 YYYY-MM-DD 형식으로 저장

    for sku, product in data["products"].items():
        if product["productFamily"] == "Compute Instance":
            attributes = product["attributes"]
            instance_type = attributes.get("instanceType")
            vcpu = attributes.get("vcpu")
            memory = attributes.get("memory")
            on_demand = data["terms"]["OnDemand"].get(sku)
            if on_demand:
                price_dimension = list(on_demand.values())[0]["priceDimensions"]
                price = list(price_dimension.values())[0]["pricePerUnit"]["USD"]
                if not vcpu or not memory or not price:
                    continue
                vcpu = int(vcpu)
                memory = float(memory.replace(" GiB", ""))
                price = float(price)
                if vcpu == 0 or memory == 0 or price == 0:
                    continue
                cloud_cost = CloudCost(
                    vendor="AWS",
                    name=instance_type,
                    region=region,
                    cpu=vcpu,
                    ram=memory,
                    cost_per_hour=price,
                    extraction_date=extraction_date,
                )
                aws_prices.append(cloud_cost)
                print(
                    f"Added: {instance_type}, {vcpu} vCPU, {memory} GB, ${price} per hour, Region: {region}"
                )
    return aws_prices


def main():
    service_code = "AmazonEC2"
    regions = [
        "us-east-1",  # US East (N. Virginia)
        # "us-east-2",  # US East (Ohio)
        # "us-west-1",  # US West (N. California)
        # "us-west-2",  # US West (Oregon)
        "ap-northeast-2",  # Asia Pacific (Seoul)
    ]

    all_prices = []
    for region in regions:
        region_prices = get_filtered_aws_prices(service_code, region)
        all_prices.extend(region_prices)

    save_to_firestore(all_prices)


if __name__ == "__main__":
    main()


# def save_to_csv(data: List[CloudCost], filename: str):
#     with open(filename, "w", newline="") as csvfile:
#         fieldnames = [
#             "vendor",
#             "name",
#             "region",
#             "cpu",
#             "ram",
#             "cost_per_hour",
#             "gpu",
#         ]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#         writer.writeheader()
#         for item in data:
#             writer.writerow(item.model_dump())
#     print(f"Data saved to {filename}")
