import requests
import json
import os
import csv
from functions.clouds.cloud_cost import CloudCost
from typing import List


def parse_azure_prices_from_file():
    with open("azure_prices.json", "r") as json_file:
        data = json.load(json_file)

    azure_prices = []
    skipped_items = 0

    for item in data["Items"]:
        try:
            description = item.get("productName", "")
            resource_group = item.get("productFamily", "")
            region = item.get("armRegionName", "global")
            cost_per_hour = item.get("unitPrice", 0)
            meter_category = item.get("meterCategory", "")

            cloud_cost = CloudCost(
                vendor="Azure",
                name=description,
                region=region,
                cost_per_hour=cost_per_hour,
            )

            if meter_category == "Virtual Machines":
                cloud_cost.cpu = item.get("cores", None)
                cloud_cost.ram = item.get("ram", None)

            if resource_group == "GPU":
                cloud_cost.gpu = "Yes"

            azure_prices.append(cloud_cost)
        except ValueError as e:
            skipped_items += 1
            print(f"Skipping item due to missing fields: {e}")

    print(f"Skipped {skipped_items} items due to missing required fields.")
    return azure_prices


def fetch_azure_sku_details(subscription_id, api_version, access_token):
    url = f"https://management.azure.com/subscriptions/{subscription_id}/providers/Microsoft.Compute/skus?api-version={api_version}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return []

    data = response.json()
    print("Data received from Azure SKU API")
    return data["value"]


def match_prices_with_skus(prices, skus):
    matched_data = []

    for sku in skus:
        if sku["resourceType"] == "virtualMachines":
            name = sku["name"]
            region = sku["locations"][0]  # Assuming the first location
            capabilities = {
                cap["name"]: cap["value"] for cap in sku["capabilities"]
            }

            # Find matching price entry
            price_entry = next(
                (p for p in prices if p.name == name and p.region == region),
                None,
            )
            if price_entry:
                price_entry.cpu = int(capabilities.get("vCPUs", 0))
                price_entry.ram = float(capabilities.get("MemoryGB", 0))
                matched_data.append(price_entry)
                print(
                    f"Matched: {name}, {capabilities.get('vCPUs')} vCPU, {capabilities.get('MemoryGB')} GB, ${price_entry.cost_per_hour} per hour"
                )

    return matched_data


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
    subscription_id = "6a132187-29c4-4fc2-a626-982dcdeb0bd0"  # Replace with your Azure subscription ID
    api_version = "2021-04-01"
    access_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ik1HTHFqOThWTkxvWGFGZnBKQ0JwZ0I0SmFLcyIsImtpZCI6Ik1HTHFqOThWTkxvWGFGZnBKQ0JwZ0I0SmFLcyJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldCIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzY2NDY4NGY4LTNmMWEtNDQwYi1iYzgyLTRhOWQ0NjM2M2E1ZS8iLCJpYXQiOjE3MjIwOTM1NTgsIm5iZiI6MTcyMjA5MzU1OCwiZXhwIjoxNzIyMDk5MTYzLCJhY3IiOiIxIiwiYWlvIjoiQVlRQWUvOFhBQUFBdGNDZGF5UVBjV0FQd012dTllZjduRVNPcUtsVWQ3VVJRK05pNzc5VWw3U3hSTHNWcXg0N0lqWlVZcGl4MUxBY1dKRnRaM0Y4NTFTUmNBUnhNcStDZHl4QWFJcmRtVGFaUHY5TWZmL0pFRmZjNzc3VXlXZlAySkRjR3FLMUk1dkc2c3Z6U0R5NDBWUXpZVVB4RUMzd0xVVjVnVVgrZW9WY2txRytGMVhGWlBZPSIsImFsdHNlY2lkIjoiMTpsaXZlLmNvbTowMDAzN0ZGRUJDRjI0RThBIiwiYW1yIjpbInB3ZCIsIm1mYSJdLCJhcHBpZCI6IjE4ZmJjYTE2LTIyMjQtNDVmNi04NWIwLWY3YmYyYjM5YjNmMyIsImFwcGlkYWNyIjoiMCIsImVtYWlsIjoieWRoMDkyNEBnbWFpbC5jb20iLCJmYW1pbHlfbmFtZSI6IllvdW4iLCJnaXZlbl9uYW1lIjoiRG9uZ0h5dW4iLCJncm91cHMiOlsiNjhmYjM4YTAtZDVjMy00NDc3LWE5NmMtN2YxYmVmOTA1MjM0Il0sImlkcCI6ImxpdmUuY29tIiwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMjIwLjcyLjE4MS4xMjIiLCJuYW1lIjoiWW91biBEb25nSHl1biIsIm9pZCI6ImFiMTJhZjg4LTY1OWYtNDM5MC1iMDk5LTZjYjNkNGNiMjg3ZCIsInB1aWQiOiIxMDAzMjAwM0FBQzg3RTIzIiwicmgiOiIwLkFjWUEtSVJHWmhvX0MwUzhna3FkUmpZNlhrWklmM2tBdXRkUHVrUGF3ZmoyTUJQR0FQay4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzdWIiOiJlRVRkX0JTQWJndE5VV0JGc09pRGVxZ05qSHhHV05uaWNGdFJLU2VPamNBIiwidGlkIjoiNjY0Njg0ZjgtM2YxYS00NDBiLWJjODItNGE5ZDQ2MzYzYTVlIiwidW5pcXVlX25hbWUiOiJsaXZlLmNvbSN5ZGgwOTI0QGdtYWlsLmNvbSIsInV0aSI6IjFmc0dUNUJoc0VhN2xOTzMwREVTQUEiLCJ2ZXIiOiIxLjAiLCJ3aWRzIjpbIjYyZTkwMzk0LTY5ZjUtNDIzNy05MTkwLTAxMjE3NzE0NWUxMCIsImI3OWZiZjRkLTNlZjktNDY4OS04MTQzLTc2YjE5NGU4NTUwOSJdLCJ4bXNfZWRvdiI6dHJ1ZSwieG1zX2lkcmVsIjoiMSA0IiwieG1zX3RjZHQiOjE3MjE5Nzk2Nzl9.jBlDANxd0UjFCIcIg-3ZJcncKj7w-2Qi-VsnIDbZEPLzBI-4r_qSfCiY1LT1UI7F148KqZsiA3bpOQt0pfJ6p5WkQ9HjIGlVZ_exe6GYrin-MFIuov1qqGLS4cveDavAl499-q7se_a4DmUc8Wx6fU2uXGkk9FmKj9Ybat_QetVBw0boB2VMQ2E-rufySdh9ba83yWMCQDCjIVqDAfjoPpIU323Lxd10FTvcivDyWkssfry-Sr2aX9_1n2GkEMvcnWvM0kHFDA1B-OavnfnOgXM2KrlKE_XPYBV49_TeuVsSsIL1zqen1fRez3pH_gmZjqYdz_rfwS7YQHzuCE7lPQ"  # You need to get this using Azure AD authentication

    # Parse retail prices from file
    retail_prices = parse_azure_prices_from_file()

    # Fetch SKU details
    sku_details = fetch_azure_sku_details(
        subscription_id, api_version, access_token
    )

    # Match prices with SKUs
    matched_prices = match_prices_with_skus(retail_prices, sku_details)

    # Save to CSV
    save_to_csv(matched_prices, "azure_matched_prices.csv")

    for price in matched_prices:
        print(price)


if __name__ == "__main__":
    main()
