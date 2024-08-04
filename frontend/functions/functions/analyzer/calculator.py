from functions.analyzer.llm import get_llm
from functions.analyzer.parser import (
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
