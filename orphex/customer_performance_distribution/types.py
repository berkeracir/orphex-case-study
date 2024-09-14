from typing import NamedTuple


class CustomerPerformanceDistributionTuple(NamedTuple):
    customer_id: str
    status: str
    type: str
    category: str
    total_revenue: float
    total_conversions: int
    count: int


class AveragedCustomerPerformanceDistributionTuple(NamedTuple):
    customer_id: str
    average_revenue: float
    average_conversions: float
