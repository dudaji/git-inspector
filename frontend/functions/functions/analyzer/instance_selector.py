from functions.analyzer.llm import get_llm
from functions.analyzer.parser import (
    InstanceResult,
    best_instance_parser,
)
from functions.analyzer.prompt import best_instance_prompt


def get_best_instance(
    aws: InstanceResult, gcp: InstanceResult, azure: InstanceResult
) -> InstanceResult:
    chain = best_instance_prompt | get_llm(temperature=0) | best_instance_parser
    return chain.invoke(
        {
            "aws": str(aws),
            "gcp": str(gcp),
            "azure": str(azure),
        }
    )
