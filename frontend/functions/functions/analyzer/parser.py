from typing import Dict, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class Instance(BaseModel):
    cloud_provider: str = Field(
        alias="cloudProvider",
        description="Name of cloud provider (GCP or AWS or Azure)",
    )
    name: str = Field(description="Name of instance type")
    cpu: float = Field(description="The number of instance cpu cores")
    ram: float = Field(description="The capacity of instance ram (GiB)")
    storage: int = Field(description="The capacity of instance storage (GiB)")
    gpu: Optional[str] = Field(
        default="None",
        description="Name of gpu model and memory (GiB) of instance. If no gpu needed, then set 'None' with string type",
    )
    region: str = Field(description="Region of instance")
    cost_per_hour: float = Field(
        alias="costPerHour", description="Cost per Hour of instance"
    )
    description: str = Field(
        description="The detailed process that led to the selection of the minimum specification instance."
    )

    class Config:
        allow_population_by_field_name = (True,)


class RepoResult(BaseModel):
    gcp: Instance = Field(description="Instance information of GCP")
    aws: Instance = Field(description="Instance information of AWS")
    azure: Instance = Field(description="Instance information of Azure")
    language_ratio: Dict[str, int] = Field(
        alias="languageRatio",
        description="The key value is the programming language used and the value is the number of bytes the programming language is used in the entire repository.",
    )

    class Config:
        allow_population_by_field_name = (True,)


class Estimate(BaseModel):
    power_consumption: str = Field(
        alias="powerConsumption",
        description="Estimated hourly power consumption while running an instance of the instance_type(kWh). Example: 0.06 kWh",
    )
    carbon_footprint: str = Field(
        alias="carbonFootprint",
        description="Estimated hourly carbon footprint while running an instance of the instance_type(kg CO2). Example: 0.025 kg CO2",
    )
    description: str = Field(
        description="Detailed calculation process for estimating power consumption and carbon emissions."
    )

    class Config:
        allow_population_by_field_name = (True,)


class CalculateResult(BaseModel):
    gcp: Estimate = Field(description="Estimate result of GCP")
    aws: Estimate = Field(description="Estimate result of AWS")
    azure: Estimate = Field(description="Estimate result of Azure")


class InstanceResult(BaseModel):
    instance: Instance = Field(description="Instance information")
    estimate: Estimate = Field(description="Estimate result of instance")


repo_result_parser = PydanticOutputParser(pydantic_object=RepoResult)
calculate_result_parser = PydanticOutputParser(pydantic_object=CalculateResult)
best_instance_parser = PydanticOutputParser(pydantic_object=InstanceResult)
