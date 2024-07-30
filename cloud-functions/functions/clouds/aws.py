import requests
import csv
from typing import List
from model import CloudCost


def get_filtered_aws_prices(service_code: str, region: str) -> List[CloudCost]:
    url = f"https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/{service_code}/current/{region}/index.json"
    print(f"Requesting data from: {url}")
    response = requests.get(url)
    data = response.json()
    print(f"Data received from AWS Pricing API for region {region}")

    aws_prices = []
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
                cloud_cost = CloudCost(
                    vendor="AWS",
                    name=instance_type,
                    region=region,
                    cost_per_hour=float(price),
                    cpu=int(vcpu) if vcpu else None,
                    ram=float(memory.replace(" GiB", "")) if memory else None,
                )
                aws_prices.append(cloud_cost)
                print(
                    f"Added: {instance_type}, {vcpu} vCPU, {memory} GB, ${price} per hour, Region: {region}"
                )
    return aws_prices


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
    service_code = "AmazonEC2"
    regions = [
        "us-east-1",
        "us-west-1",
        "us-west-2",
        "eu-west-1",
        "eu-central-1",
        "ap-southeast-1",
        "ap-northeast-1",
        "ap-south-1",
        "sa-east-1",
    ]  # Add more regions as needed

    all_prices = []
    for region in regions:
        region_prices = get_filtered_aws_prices(service_code, region)
        all_prices.extend(region_prices)

    save_to_csv(all_prices, "aws_parsed_prices.csv")

    for price in all_prices:
        print(
            f"Region: {price.region}, "
            f"Instance Type: {price.name}, "
            f"CPU: {price.cpu} core(s), "
            f"Memory: {price.ram} GB, "
            f"Price per hour: ${price.cost_per_hour:.6f}"
        )


if __name__ == "__main__":
    main()
