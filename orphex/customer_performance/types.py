from typing import NamedTuple


class CustomerPerformanceTuple(NamedTuple):
    customer_id: str
    total_revenue: float
    total_conversions: int
    count: int
