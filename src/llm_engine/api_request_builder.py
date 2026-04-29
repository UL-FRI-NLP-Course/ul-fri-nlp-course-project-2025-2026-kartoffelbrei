from typing import Any, Union

from src.llm_engine.intents import Intent
from src.backend.api_requests import APIRequests
from src.backend.route_params import RouteParams
from src.backend.format_response import format_train_type_response
from src.backend.metadata_handler import MetadataHandler

class APIRequestBuilder:
    def __init__(self, api_requests: APIRequests):
        self.api_requests = api_requests

    def send_api_request(self, intent_json: Any) -> Union[str, None]:
        intent = intent_json["intent"]

        if intent is None:
            print("No intent provided by either the LLM or the user.")
            return None

        response = ""
        match intent:
            case Intent.DELAY.value:
                response = self._build_train_information_request(intent_json)
            case Intent.ARRIVAL.value:
                response = self._build_train_information_request(intent_json)
            case Intent.DEPARTURE.value:
                response = self._build_train_information_request(intent_json)
            case Intent.ROUTE.value:
                response = self._build_route_information_request(intent_json)
            case Intent.OTHER.value:
                print("Could not provide any information related to the question.")
                return None
            case _:
                print("No valid intent was provided.")
                return None

        return format_train_type_response(response)

    def _build_train_information_request(self, intent_json: Any) -> str:
        departure_date = intent_json["departure_date"]
        train_number = intent_json["train_number"]

        return self.api_requests.get_train_information(departure_date, train_number)

    def _build_route_information_request(self, intent_json: Any) -> str:
        #departure_date = intent_json["departure_date"]

        train_stations = MetadataHandler.load_station_dict()
        departure_station = train_stations[intent_json["departure_station"]]
        destination_station = train_stations[intent_json["destination_station"]]

        print(f"Departure: {departure_station}")
        print(f"Destination: {destination_station}")

        #route_params: RouteParams = {'departure_date': departure_date}
        return self.api_requests.get_route_information(departure_station, destination_station)
