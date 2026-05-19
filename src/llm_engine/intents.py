from enum import Enum

class Intent(Enum):
    # API Intents
    JOURNEY_SEARCH = "journey_search"
    STATION_TIMETABLE = "station_timetable"
    TRAIN_STATUS = "train_status"
    # RAG Intents
    GENERAL_INFO = "general_info"
    # Out of Context
    OTHER = "other"