from typing import Any, Union, Tuple

from llm_engine.intents import Intent
from backend.api_requests import APIRequests
from backend.format_response import ResponseFormatter
from backend.metadata_handler import MetadataHandler
from backend.time_converter import TimeConverter
from backend.route_params import RouteParams

class APIRequestBuilder:
    def __init__(self, api_requests: APIRequests):
        self.api_requests = api_requests

    def send_api_request(self, intent_json: Any) -> Union[str, None]:
        intent = intent_json['intent']
        print(f"Intent: {intent}")

        if intent is None:
            print("No intent provided by either the LLM or the user.")
            return None

        match intent:
            case Intent.JOURNEY_SEARCH.value:
                return self._build_journey_search_request(intent_json)
            case Intent.STATION_TIMETABLE.value:
                return self._build_station_timetable_request(intent_json)
            case Intent.TRAIN_STATUS.value:
                return self._build_train_status_request(intent_json)
            case _:
                print("Could not provide any information related to the question.")
                return None

    def _get_intent_time(self, intent_json: Any) -> Tuple[Any, Any]:
        intent_time = intent_json['time']
        departure_time, departure_date = TimeConverter.convert_time(intent_time['raw'])
        if departure_time == None:
            departure_time = TimeConverter.get_current_time()

        if departure_date == None:
            departure_date = TimeConverter.get_current_date()

        return departure_time, departure_date

    def _get_intent_entities(self, intent_json) -> Tuple[Any, Any, Any]:
        intent_entities = intent_json['entities']

        train_number = intent_entities['train_number']

        train_stations = MetadataHandler.load_station_dict()
        departure_station = train_stations[intent_entities['departure_station']]
        destination_station = train_stations[intent_entities['destination_station']]

        return train_number, departure_station, destination_station

    def _build_journey_search_request(self, intent_json: Any) -> str:
        departure_time, departure_date = self._get_intent_time(intent_json)

        _, departure_station, destination_station = self._get_intent_entities(intent_json)

        route_params: RouteParams = {'departure_date': departure_date.isoformat()}
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
        train_number, departure_station, _ = self._get_intent_entities(intent_json)
        station_data = self.api_requests.get_live_trains(station_shortcode=departure_station)
        return ResponseFormatter.format_station_timetable_response(
            station_data=station_data,
            departure_station=departure_station
        )

    def _build_train_status_request(self, intent_json: Any) -> str:
        _, departure_date = self._get_intent_time(intent_json)

        train_number, _, _ = self._get_intent_entities(intent_json)

        result = self.api_requests.get_train_information(train_number=train_number, departure_date=departure_date)

        return ResponseFormatter.format_train_status_response(result)
