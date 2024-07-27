from pydantic import BaseModel, Field
from typing import List


class CloudCost(BaseModel):
    vendor: str
    name: str
    region: str
    cost_per_hour: float
    cpu: int = Field(default=None)  # 1, 2, 4, ...
    ram: float = Field(default=None)  # GiB
    gpu: str = Field(default=None)  #

    class Config:
        protected_namespaces = ()


# Example usage
# example = CloudCost(
#     vendor="AWS",
#     name="t2.micro",
#     region="us-east-1",
#     cost_per_hour=0.0116,
#     cpu=1,
#     ram=1.0,
# )

# print(example)
