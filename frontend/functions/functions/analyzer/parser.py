from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field


class Instance(BaseModel):
    name: str = Field(description="Name of instance type")
    cpu: str = Field(description="The number of instance cpu cores")
    memory: str = Field(description="The capacity of instance memory (GiB)")
    storage: str = Field(description="The capacity of instance storage (GiB)")
    gpu: str = Field(description="Name of gpu model and memory (GiB) of instance")


class Cost(BaseModel):
    monthly: str = Field(description="Estimated monthly measurements")
    hourly: str = Field(description="Estimated measurements per hour")


class Estimate(BaseModel):
    instance: Instance = Field(description="Instance information of Cloud Provider")
    pricing: Cost = Field(
        description="Estimated pricing while running an instance of the instance_type (USD)"
    )
    power_consumption: Cost = Field(
        description="Estimated power consumption while running an instance of the instance_type(kWh)"
    )
    carbon_footprint: Cost = Field(
        description="Estimated carbon footprint while running an instance of the instance_type(kg CO2)"
    )
    description: str = Field(
        description="A rationale and detailed explanation for estimations"
    )


class Result(BaseModel):
    gcp: Estimate = Field(description="Estimated Result of Google Cloud Platform(GCP)")
    aws: Estimate = Field(description="Estimated Result of Amazon Web Services(AWS)")
    azure: Estimate = Field(description="Estimated Result of Microsoft Azure")
    conclusion: Estimate = Field(
        description="The most appropriate among gcp, aws, and azure"
    )


output_parser = JsonOutputParser(pydantic_object=Result)
