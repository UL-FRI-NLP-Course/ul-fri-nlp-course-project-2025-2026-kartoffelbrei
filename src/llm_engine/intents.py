from enum import Enum

class Intent(Enum):
    # API Intents
    JOURNEY_SEARCH = "journey search"
    TRAIN_STATUS = "train status"
    TRAIN_TIMETABLE = "train timetable"
    STATION_TIMETABLE = "station timetable"
    # RAG Intents
    FARE_AND_TICKET = "fare and ticket"
    TRAVEL_POLICY = "travel policy"
    STATION_INFO = "station info"
    RAILWAY_INFO = "railway info"
    BOOKING_SUPPORT = "booking support"
    GREETING = "greeting"
    OUT_OF_SCOPE = "out of scope"