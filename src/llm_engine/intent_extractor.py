import re

from typing import Any, Union, Tuple, Dict
from datetime import date, time

from backend.time_converter import TimeConverter
from backend.metadata_handler import MetadataHandler

class IntentExtractor:

    @staticmethod
    def get_intent(intent_json: Any) -> str:
        intent = intent_json.get('intent')

        if intent is None or intent == 'null':
            return ""

        return intent

    @staticmethod
    def get_intent_time(intent_json: Any) -> Tuple[Union[time, None], Union[date, None]]:
        intent_time = intent_json.get('time')
        if (
                intent_time is not None
                and intent_time.get('raw') is not None
                and intent_time.get('raw') != 'null'
        ):
            departure_time, departure_date = TimeConverter.convert_time(intent_time.get('raw'))
        else:
            departure_time, departure_date = None, None

        if departure_time is None:
            departure_time = TimeConverter.get_current_time()

        if departure_date is None:
            departure_date = TimeConverter.get_current_date()

        return departure_time, departure_date

    @staticmethod
    def _extract_train_number(value: Union[str, None]) -> Union[str, None]:
        if not value or value == 'null':
            return None

        value = value.strip()

        match = re.search(r"\d+", value)

        return match.group(0) if match else None

    @staticmethod
    def get_intent_entities(intent_json) -> Tuple[Any, Any, Any]:
        intent_entities: Dict[str, Any] = intent_json.get('entities')

        train_number = IntentExtractor._extract_train_number(intent_entities.get('train_number'))

        train_stations = MetadataHandler.load_station_dict()

        departure_station = None
        if (
                intent_entities.get('departure_station') is not None
                and intent_entities.get('departure_station') != 'null'
        ):
            departure_station = train_stations[intent_entities.get('departure_station')]

        destination_station = None
        if (
                intent_entities.get('destination_station') is not None
                and intent_entities.get('destination_station') != 'null'
        ):
            destination_station = train_stations[intent_entities.get('destination_station')]

        return train_number, departure_station, destination_station