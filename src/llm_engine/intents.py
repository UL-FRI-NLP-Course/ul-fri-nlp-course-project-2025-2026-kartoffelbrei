from enum import Enum

class Intent(Enum):
    DELAY = "delay"
    ARRIVAL = "arrival"
    DEPARTURE = "departure"
    ROUTE = "route"
    OTHER = "other"
