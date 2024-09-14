from typing import NamedTuple


class CustomerConversionRateTuple(NamedTuple):
    customer_id: str
    total_revenue: float
    total_conversions: int
