import requests
import json


def fetch_azure_sku_info():
    url = "https://management.azure.com/subscriptions/{subscriptionId}/providers/Microsoft.Compute/skus?api-version=2024-03-02"
    headers = {"Authorization": "Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    sku_data = response.json()
    sku_info = {}

    for sku in sku_data.get("value", []):
        if sku["resourceType"] == "virtualMachines":
            name = sku["name"]
            capabilities = {
                cap["name"]: cap["value"] for cap in sku.get("capabilities", [])
            }
            vcpu = capabilities.get("vCPUs", "N/A")
            memory = capabilities.get("MemoryGB", "N/A")
            sku_info[name] = {"vcpu": vcpu, "memory": memory}

    with open("azure_sku_info.json", "w") as json_file:
        json.dump(sku_info, json_file, indent=4)

    print(f"Data saved to azure_sku_info.json with {len(sku_info)} items.")


def main():
    fetch_azure_sku_info()


if __name__ == "__main__":
    main()
