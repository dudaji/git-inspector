from functions.analyzer.llm import get_llm
from functions.analyzer.parser import (
    RepoResult,
    calculate_result_parser,
    CalculateResult,
)
from functions.analyzer.prompt import calculation_prompt


def calculate_power_and_carbon(repo_result: RepoResult) -> CalculateResult:
    chain = calculation_prompt | get_llm(temperature=0.2) | calculate_result_parser
    return chain.invoke(
        {
            "aws": str(repo_result.aws),
            "gcp": str(repo_result.gcp),
            "azure": str(repo_result.azure),
        }
    )
