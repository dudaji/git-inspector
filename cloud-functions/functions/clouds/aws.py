import requests


def get_filtered_aws_prices(service_code, region):
    url = f"https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/{service_code}/current/{region}/index.json"
    print(f"Requesting data from: {url}")
    response = requests.get(url)
    data = response.json()
    print("Data received from AWS Pricing API")

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
                aws_prices.append(
                    {
                        "instance_type": instance_type,
                        "vcpu": int(vcpu) if vcpu else None,
                        "memory": float(memory.replace(" GiB", ""))
                        if memory
                        else None,
                        "price_per_hour": float(price),
                    }
                )
                print(
                    f"Added: {instance_type}, {vcpu} vCPU, {memory} GB, ${price} per hour"
                )
    return aws_prices


def main():
    service_code = "AmazonEC2"
    region = "us-east-1"  # Change as region code -> Regional data is 300MB round, but all data is over 5GB, be careful to use
    aws_prices = get_filtered_aws_prices(service_code, region)
    for price in aws_prices:
        print(
            f"Instance Type: {price['instance_type']}, "
            f"CPU: {price['vcpu']} core(s), "
            f"Memory: {price['memory']} GB, "
            f"Price per hour: ${price['price_per_hour']:.6f}"
        )


if __name__ == "__main__":
    main()

"""

Instance Type: d3en.6xlarge, CPU: 24 core(s), Memory: 96.0 GB, Price per hour: $3.750000
Instance Type: r5d.2xlarge, CPU: 8 core(s), Memory: 64.0 GB, Price per hour: $0.711000
Instance Type: r6idn.xlarge, CPU: 4 core(s), Memory: 32.0 GB, Price per hour: $0.998380
Instance Type: r5b.8xlarge, CPU: 32 core(s), Memory: 256.0 GB, Price per hour: $0.000000
Instance Type: r6idn.4xlarge, CPU: 16 core(s), Memory: 128.0 GB, Price per hour: $0.000000
Instance Type: x2iedn.4xlarge, CPU: 16 core(s), Memory: 512.0 GB, Price per hour: $3.334500
Instance Type: inf1.24xlarge, CPU: 96 core(s), Memory: 192.0 GB, Price per hour: $41.005000
Instance Type: r5dn.large, CPU: 2 core(s), Memory: 16.0 GB, Price per hour: $0.000000
Instance Type: r6i.12xlarge, CPU: 48 core(s), Memory: 384.0 GB, Price per hour: $4.214400
Instance Type: r5n.large, CPU: 2 core(s), Memory: 16.0 GB, Price per hour: $0.000000
Instance Type: x2idn.16xlarge, CPU: 64 core(s), Memory: 1024.0 GB, Price per hour: $0.000000
Instance Type: r7a.2xlarge, CPU: 8 core(s), Memory: 64.0 GB, Price per hour: $1.936600
Instance Type: g4dn.2xlarge, CPU: 8 core(s), Memory: 32.0 GB, Price per hour: $0.000000
"""
