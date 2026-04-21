from enum import Enum

class FintrafficEndpoints(Enum):
    BASE = "https://rata.digitraffic.fi/api/v1/"
    TRAINS = BASE + "trains"
    LIVE_TRAINS = BASE + "live-trains"
    LIVE_TRAINS_STATION = BASE + "live-trains/station"