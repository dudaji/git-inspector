from typing import List
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


def select_best_instance(instances: List[InstanceResult]) -> InstanceResult:
    # Normalize cost and carbon footprint to a 0-1 scale
    costs = [instance.instance.cost_per_hour for instance in instances]
    power_consumptions = [
        float(instance.estimate.power_consumption.split(" ", 1)[0])
        for instance in instances
    ]
    footprints = [
        float(instance.estimate.carbon_footprint.split(" ", 1)[0])
        for instance in instances
    ]
    print(power_consumptions)
    print(footprints)

    min_cost, max_cost = min(costs), max(costs)
    min_footprint, max_footprint = min(footprints), max(footprints)
    min_power, max_power = min(power_consumptions), max(power_consumptions)

    def normalize(value, min_value, max_value):
        return (
            (value - min_value) / (max_value - min_value)
            if max_value > min_value
            else 0
        )

    best_instance = None
    best_score = float("inf")

    for instance in instances:
        normalized_cost = normalize(instance.instance.cost_per_hour, min_cost, max_cost)
        normalized_footprint = normalize(
            float(instance.estimate.carbon_footprint.split(" ", 1)[0]),
            min_footprint,
            max_footprint,
        )
        normalized_power = normalize(
            float(instance.estimate.power_consumption.split(" ", 1)[0]),
            min_power,
            max_power,
        )

        # Adjust the weightage if needed
        score = normalized_cost + normalized_footprint + normalized_power

        if score < best_score:
            best_score = score
            best_instance = instance

    return best_instance
