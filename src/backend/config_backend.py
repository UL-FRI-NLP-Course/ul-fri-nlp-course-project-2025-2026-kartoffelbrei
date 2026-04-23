from dataclasses import dataclass

@dataclass
class ConfigBackend():
    BASE: str = "https://rata.digitraffic.fi/api/v1/"
    TRAINS: str = BASE + "trains"
    LIVE_TRAINS: str = BASE + "live-trains"
    LIVE_TRAINS_STATION: str = BASE + "live-trains/station"
    URLS = ["https://www.vr.fi/en/terms-and-conditions", "https://www.vr.fi/en/accessibility-statement" 
    ]