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


def analyze_full_steps(
    clone_url: str, branch: str = "main", folder: str = ""
) -> FinalResponse:
    repo_result = analyze_repo(clone_url, branch, folder)
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
