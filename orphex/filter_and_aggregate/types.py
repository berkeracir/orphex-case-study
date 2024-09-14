from typing import NamedTuple, Optional


class FilterAndAggregateTuple(NamedTuple):
    customer_id: str
    status: Optional[str]
    type: Optional[str]
    category: Optional[str]
    average_revenue: float
    average_conversions: float
