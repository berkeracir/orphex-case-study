from typing import NamedTuple


class PerformanceDistributionTuple(NamedTuple):
    status: str
    type: str
    category: str
    total_revenue: float
    total_conversions: int
    count: int


class TypeAndCategoryPerformanceDistributionTuple(NamedTuple):
    type: str
    category: str
    total_revenue: float
    total_conversions: int
