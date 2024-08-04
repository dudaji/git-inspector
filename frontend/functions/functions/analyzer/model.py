from pydantic import BaseModel, Field


class DetailedScore(BaseModel):
    cost_efficiency: float = Field(description="Cost efficiency score")
    performance: float = Field(description="Performance score")
    environmental_impact: float = Field(description="Environmental impact score")
    total: float = Field(description="Total score")


class Scores(BaseModel):
    winner: str = Field(description="Name of the cloud provider with the highest score")
    gcp: DetailedScore = Field(description="Detailed score of GCP")
    aws: DetailedScore = Field(description="Detailed score of AWS")
    azure: DetailedScore = Field(description="Detailed score of Azure")
    language: float = Field(description="Environmental score of repository code")


class GeminiAnalysis(BaseModel):
    repo_url: str = Field(description="The URL requested by the client")
    branch: str = Field(description="The branch name requested by the client")
    directory: str = Field(description="The directory name requested by the client")
    result: dict = Field(description="Gemini generated result")
    scores: Scores = Field(
        description="The calculated cloud provider scores from result"
    )
