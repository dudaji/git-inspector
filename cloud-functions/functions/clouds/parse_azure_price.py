import json
import re


def parse_azure_prices_from_file():
    with open("filtered_azure_prices.json", "r") as json_file:
        data = json.load(json_file)

    azure_prices = []
    for item in data:
        instance_type = item.get("armSkuName", "N/A")
        if instance_type == "N/A":
            continue

        # Extract vCPU and memory from productName or skuName
        product_name = item.get("productName", "")
        sku_name = item.get("skuName", "")
        vcpu = "N/A"
        memory = "N/A"

        vcpu_match = re.search(r"(\d+)\s*vCPU", product_name)
        if not vcpu_match:
            vcpu_match = re.search(r"(\d+)\s*vCore", sku_name)
        if vcpu_match:
            vcpu = vcpu_match.group(1)

        memory_match = re.search(r"(\d+(\.\d+)?)\s*GB", product_name)
        if memory_match:
            memory = memory_match.group(1)

        price_per_hour = item.get("retailPrice", "N/A")
        region = item.get("armRegionName", "N/A")

        azure_prices.append(
            {
                "instance_type": instance_type,
                "vcpu": vcpu,
                "memory": memory,
                "price_per_hour": price_per_hour,
                "region": region,
            }
        )
        print(
            f"Added: {instance_type}, {vcpu} vCPU, {memory} GB, ${price_per_hour} per hour, Region: {region}"
        )

    return azure_prices


def main():
    azure_prices = parse_azure_prices_from_file()
    for price in azure_prices:
        print(
            f"Instance Type: {price['instance_type']}, "
            f"Region: {price['region']}, "
            f"CPU: {price['vcpu']} core(s), "
            f"Memory: {price['memory']} GB, "
            f"Price per hour: ${price['price_per_hour']:.6f}"
        )


if __name__ == "__main__":
    main()
