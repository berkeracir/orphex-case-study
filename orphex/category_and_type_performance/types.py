from typing import NamedTuple


class CategoryAndTypePerformanceTuple(NamedTuple):
    type: str
    category: str
    total_revenue: float
    total_conversions: int
