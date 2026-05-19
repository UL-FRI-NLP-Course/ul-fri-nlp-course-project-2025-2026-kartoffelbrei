from enum import Enum

class Intent(Enum):
    # API Intents
    JOURNEY_SEARCH = "journey_search"
    TRAIN_STATUS = "train_status"
    TRAIN_TIMETABLE = "train_timetable"
    STATION_TIMETABLE = "station_timetable"
    # RAG Intents
    OTHER = "other"