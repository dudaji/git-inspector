from pydantic import BaseModel, Field
from typing import Optional
from analyzer.parser import Instance, Cost, Estimate, Result

class GitStore(BaseModel):
    repo_url: str = Field(description="The URL requested by the client")
    gcp: Estimate = Field(description="Estimated Result of Google Cloud Platform(GCP)")
    aws: Estimate = Field(description="Estimated Result of Amazon Web Services(AWS)")
    azure: Estimate = Field(description="Estimated Result of Microsoft Azure")
    conclusion: Estimate = Field(description="The most appropriate among gcp, aws, and azure")
    score: float = Field(description="The score assigned to the result")
    rank: int

