from typing import List
from functions.analyzer.llm import get_llm
from functions.analyzer.parser import (
    Estimate,
    Instance,
    RepoResult,
    calculate_result_parser,
    CalculateResult,
)
from functions.analyzer.prompt import calculation_prompt

import json


def instance_without_description(instance: Instance):
    instance_dict = json.loads(instance.json())
    del instance_dict["description"]
    return json.dumps(instance_dict)


def calculate_power_and_carbon(repo_result: RepoResult) -> CalculateResult:
    chain = calculation_prompt | get_llm(temperature=0.2) | calculate_result_parser
    aws = instance_without_description(repo_result.aws)
    gcp = instance_without_description(repo_result.gcp)
    azure = instance_without_description(repo_result.azure)
    return chain.invoke(
        {
            "aws": aws,
            "gcp": gcp,
            "azure": azure,
        }
    )


def estimate_environment(
    aws_instance: Instance, gcp_instance: Instance, azure_instance: Instance
) -> CalculateResult:
    chain = calculation_prompt | get_llm(temperature=0.2) | calculate_result_parser
    aws = instance_without_description(aws_instance)
    gcp = instance_without_description(gcp_instance)
    azure = instance_without_description(azure_instance)
    return chain.invoke(
        {
            "aws": aws,
            "gcp": gcp,
            "azure": azure,
        }
    )


def estimate_environment_mock(
    aws_instance: Instance, gcp_instance: Instance, azure_instance: Instance
) -> CalculateResult:
    return CalculateResult(
        gcp=Estimate(
            power_consumption="0.05 kWh",
            carbon_footprint="0.015 kg CO2",
            description="Based on the GCP Carbon Footprint calculator and assuming a e2-medium instance in us-central1 region (highly efficient cooling and a carbon free energy source), the estimated power consumption is 50W/hr (0.05 kWh) and the carbon footprint is 0.015 kg CO2 per hour.  \n\nReferences:\n* GCP Carbon Footprint calculator: https://cloud.google.com/carbon-footprint",
        ),
        aws=Estimate(
            power_consumption="0.06 kWh",
            carbon_footprint="0.026 kg CO2",
            description="Assuming a t3.medium instance consumes approximately 60W/hr (0.06 kWh) based on industry averages for similar instance types and AWS's commitment to renewable energy. The carbon footprint is estimated using the average carbon intensity of the US electricity grid (0.43 kg CO2/kWh) from the EPA. \n\nReferences:\n* EPA Greenhouse Gas Equivalencies Calculator: https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator",
        ),
        azure=Estimate(
            power_consumption="0.055 kWh",
            carbon_footprint="0.024 kg CO2",
            description="Based on an estimated power consumption of 55W/hr (0.055 kWh) for a Standard_B2s instance, derived from Azure's sustainability efforts and industry benchmarks.  The carbon footprint is calculated using the average carbon intensity of the US electricity grid (0.43 kg CO2/kWh) from the EPA. \n\nReferences:\n* Microsoft Azure Sustainability: https://azure.microsoft.com/en-us/global-infrastructure/sustainability/\n* EPA Greenhouse Gas Equivalencies Calculator: https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator",
        ),
    )
