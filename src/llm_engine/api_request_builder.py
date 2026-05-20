from typing import Any

from llm_engine.intents import Intent
from llm_engine.intent_extractor import IntentExtractor
from backend.api_requests import APIRequests
from backend.format_response import ResponseFormatter
from backend.route_params import RouteParams

class APIRequestBuilder:
    def __init__(self, api_requests: APIRequests):
        self.api_requests = api_requests

    def send_api_request(self, intent_json: Any) -> str:
        intent = IntentExtractor.get_intent(intent_json)

        if intent == "":
            print("No intent provided by either the LLM or the user.")
            return ""

        match intent:
            case Intent.JOURNEY_SEARCH.value:
                return self._build_journey_search_request(intent_json)
            case Intent.STATION_TIMETABLE.value:
                return self._build_station_timetable_request(intent_json)
            case Intent.TRAIN_STATUS.value:
                return self._build_train_status_request(intent_json)
            case _:
                print("Could not provide any information related to the question.")
                return ""

    def _build_journey_search_request(self, intent_json: Any) -> str:
        departure_time, departure_date = IntentExtractor.get_intent_time(intent_json)

        _, departure_station, destination_station = IntentExtractor.get_intent_entities(intent_json)

        if departure_station is None or destination_station is None:
            return ""

        route_params: RouteParams = {'departure_date': departure_date}
        train_data = self.api_requests.get_journey_information(
            departure_station=departure_station,
            destination_station=destination_station,
            params=route_params)
        return ResponseFormatter.format_journey_response(
            train_data=train_data,
            departure_station=departure_station,
            destination_station=destination_station,
            current_time=departure_time,
        )

    def _build_station_timetable_request(self, intent_json: Any) -> str:
        _, departure_station, destination_station = IntentExtractor.get_intent_entities(intent_json)

        if departure_station is None and destination_station is None:
            return ""

        station = departure_station if departure_station is not None else destination_station
        station_data = self.api_requests.get_live_trains(station_shortcode=station)
        return ResponseFormatter.format_station_timetable_response(
            station_data=station_data,
            departure_station=station
        )

    def _build_train_status_request(self, intent_json: Any) -> str:
        _, departure_date = IntentExtractor.get_intent_time(intent_json)

        train_number, _, _ = IntentExtractor.get_intent_entities(intent_json)

        if train_number is None:
            return ""

        result = self.api_requests.get_train_status(train_number=train_number, departure_date=departure_date)

        return ResponseFormatter.format_train_status_response(result)
