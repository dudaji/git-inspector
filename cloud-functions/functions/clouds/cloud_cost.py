from pydantic import BaseModel, Field
from typing import List, Optional


class CloudCost(BaseModel):
    vendor: str
    name: str
    region: str
    cpu: float  # 1, 2, 4, ...
    ram: float  # GiB
    cost_per_hour: float
    gpu: Optional[str] = Field(default=None)  #
    extraction_date: str  # 데이터를 추출한 날짜

    def to_dict(self):
        return {
            "vendor": self.vendor,
            "name": self.name,
            "region": self.region,
            "cpu": self.cpu,
            "ram": self.ram,
            "cost_per_hour": self.cost_per_hour,
            "extraction_date": self.extraction_date,
        }