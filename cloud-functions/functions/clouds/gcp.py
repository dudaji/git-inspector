from google.oauth2 import service_account
from googleapiclient.discovery import build
import re


def get_gcp_prices():
    """Retrieves GCP Compute Engine pricing information.

    This function retrieves pricing information for Google Cloud Platform (GCP)
    Compute Engine instances. It uses a service account for authentication
    and interacts with the Cloud Billing API.

    Returns:
        list: A list of dictionaries containing information about each relevant
              Compute Engine instance type, including:
                - instance_type: The type of virtual machine (e.g., n1-standard-1)
                - region: The region where the instance is available
                - cpu: Number of virtual CPUs (vCPU)
                - memory: Memory size in GiB
                - gpu: Presence of a GPU (Yes/No)
                - price_per_hour: The estimated price per hour
    """

    # Update with the path to your service account JSON file
    SERVICE_ACCOUNT_FILE = "git-inspector-dudaji-gcp.json"

    # Authenticate with service account
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )

    # Build
    #  Cloud Billing service object
    service = build("cloudbilling", "v1", credentials=credentials)

    # Request SKU information for Compute Engine service
    gcp_prices = []
    request = service.services().skus().list(parent="services/6F81-5844-456A")

    while request is not None:
        print("Sending API request...")
        response = request.execute()
        print("API response received")

        for sku in response.get("skus", []):
            if "Compute" in sku["category"]["resourceFamily"]:
                # Extract pricing information and instance details using regular expressions
                pricing_info = sku["pricingInfo"][0]["pricingExpression"][
                    "tieredRates"
                ][0]["unitPrice"]
                units = int(pricing_info.get("units", "0"))
                nanos = int(pricing_info.get("nanos", "0"))
                price = units + nanos / 1e9

                instance_type_match = re.search(
                    r"([A-Z]\d[\w-]*)", sku["description"]
                )
                if not instance_type_match:
                    print(
                        f"Skipping SKU due to unmatched instance type: {sku['description']}"
                    )
                    continue

                instance_type = instance_type_match.group(1)
                vcpu_match = re.search(r"(\d+) vCPU", sku["description"])
                memory_match = re.search(
                    r"(\d+(\.\d+)?) GiB", sku["description"]
                )

                if vcpu_match and memory_match:
                    vcpu = int(vcpu_match.group(1))
                    memory = float(memory_match.group(1))
                else:
                    print(
                        f"Skipping SKU due to missing vCPU or memory: {sku['description']}"
                    )
                    continue

                gpu = "Yes" if sku["category"].get("gpu") else "No"
                region = (
                    sku["serviceRegions"][0]
                    if sku["serviceRegions"]
                    else "Global"
                )

                # Skip Preemptible or on-demand SKUs (may not be suitable for consistent needs)
                if (
                    "Preemptible" in sku["description"]
                    or "onDemand" in sku["description"]
                ):
                    continue

                # Add details to price information dictionary
                gcp_prices.append(
                    {
                        "instance_type": instance_type,
                        "region": region,
                        "cpu": vcpu,
                        "memory": memory,
                        "gpu": gpu,
                        "price_per_hour": price,
                    }
                )

        request = (
            service.services()
            .skus()
            .list_next(previous_request=request, previous_response=response)
        )

    return gcp_prices


def main():
    """Prints GCP Compute Engine pricing information."""

    gcp_prices = get_gcp_prices()
    for price in gcp_prices:
        print(
            f"Instance Type: {price['instance_type']}, "
            f"Region: {price['region']}, "
            f"CPU: {price['cpu']} core(s), "
            f"Memory: {price['memory']} GiB, "
            f"GPU: {price['gpu']}, "
        )
