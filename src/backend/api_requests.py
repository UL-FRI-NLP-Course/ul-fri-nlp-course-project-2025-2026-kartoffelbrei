import requests
from requests import Response
from typing import Optional, Mapping, Any
from urllib.parse import urlencode

from src.backend.config_backend import ConfigBackend as Config
from src.backend.live_train_params import LiveTrainParams
from src.backend.route_params import RouteParams

class APIRequests:

    @staticmethod
    def _build_url(extensions: list[str]) -> str:
        return "/".join(extensions)

    @staticmethod
    def _add_params_to_url(url: str, params: Mapping[str, Any]) -> str:
        return url + "?" + urlencode(params)

    @staticmethod
    def _return_response(response: Response) -> Any:
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code)
            return None

    def get_live_trains(
            self,
            station_shortcode: Optional[str] = None,
            params: Optional[LiveTrainParams] = None
    ) -> Optional[str]:
        if station_shortcode is None:
            url = Config.LIVE_TRAINS
        else:
            url = self._build_url([Config.LIVE_TRAINS_STATION, station_shortcode])

            if params is not None:
                url = self._add_params_to_url(url, params)

        return self._return_response(requests.get(url))

    def get_train_information(
            self, departure_date: str,
            train_number: Optional[int] = None
    ) -> str | None:
        if train_number is None:
            url = self._build_url([Config.TRAINS, departure_date])
        else:
            url = self._build_url([Config.TRAINS, departure_date, str(train_number)])

        return self._return_response(requests.get(url))

    def get_route_information(
            self,
            departure_station: str,
            destination_station: str,
            params: Optional[RouteParams] = None
    ):
        url = self._build_url([Config.LIVE_TRAINS_STATION, departure_station, destination_station])

        if params is not None:
            url = self._add_params_to_url(url, params)

        return self._return_response(requests.get(url))