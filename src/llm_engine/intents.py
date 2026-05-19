from enum import Enum

class Intent(Enum):
    # API Intents
    JOURNEY_SEARCH = "journey search"
    TRAIN_STATUS = "train status"
    TRAIN_TIMETABLE = "train timetable"
    STATION_TIMETABLE = "station timetable"
    # RAG Intents
    OTHER = "other"