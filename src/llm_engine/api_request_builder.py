from typing import Any, Union

from llm_engine.intents import Intent
from backend.api_requests import APIRequests
from backend.format_response import ResponseFormatter
from backend.metadata_handler import MetadataHandler

class APIRequestBuilder:
    def __init__(self, api_requests: APIRequests):
        self.api_requests = api_requests

    def send_api_request(self, intent_json: Any) -> Union[str, None]:
        intent = intent_json["intent"]

        if intent is None:
            print("No intent provided by either the LLM or the user.")
            return None

        match intent:
            case Intent.JOURNEY.value:
                return self._build_train_information_request(intent_json)
            case Intent.TRAIN_STATUS.value:
                return self._build_train_information_request(intent_json)
            case Intent.TRAIN_TIMETABLE.value:
                return self._build_train_information_request(intent_json)
            case Intent.STATION_TIMETABLE.value:
                return self._build_route_information_request(intent_json)
            case Intent.OUT_OF_SCOPE.value:
                print("Could not provide any information related to the question.")
                return None
            case _:
                print("No valid intent was provided.")
                return None

    def _build_train_information_request(self, intent_json: Any) -> str:
        departure_date = intent_json["departure_date"]
        train_number = intent_json["train_number"]

        result = self.api_requests.get_train_information(train_number=train_number)
        return ResponseFormatter.format_train_status_response(train_data=result)

    def _build_route_information_request(self, intent_json: Any) -> str:
        #departure_date = intent_json["departure_date"]

        train_stations = MetadataHandler.load_station_dict()
        departure_station = train_stations[intent_json["departure_station"]]
        destination_station = train_stations[intent_json["destination_station"]]

        #route_params: RouteParams = {'departure_date': departure_date}
        result = self.api_requests.get_route_information(departure_station, destination_station)
        return ResponseFormatter.format_journey_response(
            train_data=result,
            departure_station=departure_station,
            destination_station=destination_station
        )
