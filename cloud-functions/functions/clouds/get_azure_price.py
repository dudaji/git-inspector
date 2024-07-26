import requests
import json


def fetch_and_save_filtered_azure_prices():
    url = "https://prices.azure.com/api/retail/prices"
    params = {
        "$filter": "serviceName eq 'Virtual Machines' and armRegionName eq 'eastus'",
        "$top": 100,  # Adjust the number of items per page
    }
    all_data = []
    page_count = 0

    while url:
        print(f"Requesting data from: {url}")
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Failed to retrieve data: {response.status_code}")
            print(response.text)  # Print the response text for debugging
            break

        data = response.json()
        all_data.extend(data.get("Items", []))

        url = data.get("NextPageLink")
        params = {}  # Clear params for next requests
        page_count += 1

    # Save data to a JSON file
    with open("filtered_azure_prices.json", "w") as json_file:
        json.dump(all_data, json_file, indent=4)

    print(
        f"Data saved to filtered_azure_prices.json with {len(all_data)} items."
    )


def main():
    fetch_and_save_filtered_azure_prices()


if __name__ == "__main__":
    main()
