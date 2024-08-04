from typing import Dict
from langchain_core.pydantic_v1 import BaseModel, Field
from functions.analyzer.calculator import calculate_power_and_carbon
from functions.analyzer.instance_selector import select_best_instance
from functions.analyzer.parser import InstanceResult
from functions.analyzer.pricing import get_cheapest_instance
from functions.analyzer.repo_analyzer import analyze_repo


class FinalResponse(BaseModel):
    aws: InstanceResult = Field(description="Information of instance and estimation")
    gcp: InstanceResult = Field(description="Information of instance and estimation")
    azure: InstanceResult = Field(description="Information of instance and estimation")
    conclusion: InstanceResult = Field(
        description="The most appropriate among gcp, aws, and azure"
    )
    language_ratio: Dict[str, int] = Field(
        description="The key value is the programming language used and the value is the number of bytes the programming language is used in the entire repository."
    )


def analyze_full_steps(repo_path: str, directory: str = "") -> FinalResponse:
    repo_result = analyze_repo(repo_path, directory)
    repo_result.aws = get_cheapest_instance(repo_result.aws)
    repo_result.gcp = get_cheapest_instance(repo_result.gcp)

    calculate_result = calculate_power_and_carbon(repo_result)

    aws = InstanceResult(instance=repo_result.aws, estimate=calculate_result.aws)
    gcp = InstanceResult(instance=repo_result.gcp, estimate=calculate_result.gcp)
    azure = InstanceResult(instance=repo_result.azure, estimate=calculate_result.azure)

    best_instance = select_best_instance([aws, gcp, azure])

    return FinalResponse(
        aws=aws,
        gcp=gcp,
        azure=azure,
        conclusion=best_instance,
        language_ratio=repo_result.language_ratio,
    )


def analyze_with_mock(repo_path: str, directory: str = "") -> FinalResponse:
    return FinalResponse(
        **{
            "aws": {
                "instance": {
                    "cloud_provider": "AWS",
                    "name": "t3.medium",
                    "cpu": 2,
                    "ram": 4.0,
                    "storage": 10,
                    "gpu": None,
                    "region": "us-east-1",
                    "cost_per_hour": 0.0441,
                    "description": "This application requires a minimum of 2 vCPUs and 2GB of RAM to run. A simple Java application with Spring Boot and MySQL usually doesn't demand high CPU or memory resources. Therefore, a t3.medium instance, which provides a balance of performance and cost, is chosen. 10GB of storage is sufficient for this application and its data. The application does not require a GPU. The us-east-1 region offers a good balance of cost and latency for many users.",
                },
                "estimate": {
                    "power_consumption": "0.06 kWh",
                    "carbon_footprint": "0.025 kg CO2",
                    "description": "Based on the AWS power consumption data for t3.medium instance and considering a sustained CPU utilization of 40%, the estimated hourly power consumption is 0.06 kWh. This calculation considers the PUE of AWS data centers. The carbon footprint is estimated to be 0.025 kg CO2 per hour, based on the region's grid carbon intensity and AWS's sustainability initiatives.",
                },
            },
            "gcp": {
                "instance": {
                    "cloud_provider": "GCP",
                    "name": "e2-medium",
                    "cpu": 1,
                    "ram": 4.0,
                    "storage": 10,
                    "gpu": None,
                    "region": "us-central1",
                    "cost_per_hour": 0.0169861111111111,
                    "description": "This application requires a minimum of 2 vCPUs and 2GB of RAM to run. A simple Java application with Spring Boot and MySQL usually doesn't demand high CPU or memory resources. Therefore, an e2-medium instance, which provides a balance of performance and cost, is chosen. 10GB of storage is sufficient for this application and its data. The application does not require a GPU. The us-central1 region offers a good balance of cost and latency for many users.",
                },
                "estimate": {
                    "power_consumption": "0.05 kWh",
                    "carbon_footprint": "0.01 kg CO2",
                    "description": "Based on the GCP Carbon Footprint calculator and considering the e2-medium instance located in us-central1 region has a sustained CPU utilization of 40%, the estimated hourly power consumption is 0.05 kWh. This calculation considers the PUE of Google Cloud's data centers. The carbon footprint is estimated to be 0.01 kg CO2 per hour, based on the region's grid carbon intensity and Google's commitment to renewable energy.",
                },
            },
            "azure": {
                "instance": {
                    "cloud_provider": "Azure",
                    "name": "Standard_B2s",
                    "cpu": 2,
                    "ram": 4.0,
                    "storage": 10,
                    "gpu": "None",
                    "region": "eastus",
                    "cost_per_hour": 0.0456,
                    "description": "This application requires a minimum of 2 vCPUs and 2GB of RAM to run. A simple Java application with Spring Boot and MySQL usually doesn't demand high CPU or memory resources. Therefore, a Standard_B2s instance, which provides a balance of performance and cost, is chosen. 10GB of storage is sufficient for this application and its data. The application does not require a GPU. The eastus region offers a good balance of cost and latency for many users.",
                },
                "estimate": {
                    "power_consumption": "0.07 kWh",
                    "carbon_footprint": "0.03 kg CO2",
                    "description": "Based on the Azure Sustainability Calculator and considering the Standard_B2s instance located in the eastus region has a sustained CPU utilization of 40%, the estimated hourly power consumption is 0.07 kWh. This calculation considers the PUE of Azure's data centers. The carbon footprint is estimated to be 0.03 kg CO2 per hour, based on the region's grid carbon intensity and Microsoft's commitment to renewable energy.",
                },
            },
            "conclusion": {
                "instance": {
                    "cloud_provider": "GCP",
                    "name": "e2-medium",
                    "cpu": 1,
                    "ram": 4.0,
                    "storage": 10,
                    "gpu": "None",
                    "region": "us-central1",
                    "cost_per_hour": 0.0169861111111111,
                    "description": "This application requires a minimum of 2 vCPUs and 2GB of RAM to run. A simple Java application with Spring Boot and MySQL usually doesn't demand high CPU or memory resources. Therefore, an e2-medium instance, which provides a balance of performance and cost, is chosen. 10GB of storage is sufficient for this application and its data. The application does not require a GPU. The us-central1 region offers a good balance of cost and latency for many users.",
                },
                "estimate": {
                    "power_consumption": "0.05 kWh",
                    "carbon_footprint": "0.01 kg CO2",
                    "description": "Based on the GCP Carbon Footprint calculator and considering the e2-medium instance located in us-central1 region has a sustained CPU utilization of 40%, the estimated hourly power consumption is 0.05 kWh. This calculation considers the PUE of Google Cloud's data centers. The carbon footprint is estimated to be 0.01 kg CO2 per hour, based on the region's grid carbon intensity and Google's commitment to renewable energy.",
                },
            },
            "language_ratio": {
                "Kotlin": 1754,
                "Properties": 1056,
                "YAML": 810,
                "Shell": 3607,
                "Batch": 2830,
                "JSON": 2742,
            },
        }
    )
