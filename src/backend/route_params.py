from typing import Optional, TypedDict
from datetime import date, datetime

class RouteParams(TypedDict, total = False):
    departure_date: Optional[date]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    limit: Optional[int]
    include_nonstopping: Optional[bool]