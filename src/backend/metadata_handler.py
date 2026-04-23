import os.path
import requests
import json
from typing import Any
from pathlib import Path

base_dir = Path(__file__).resolve().parent
metadata_path: str = os.path.join(base_dir.parent, "metadata")

class MetadataHandler:

    @staticmethod
    def _get_data(url: str) -> Any:
        return requests.get(url).json()

    @staticmethod
    def _write_json(data: Any, name: str) -> None:
        with open(os.path.join(metadata_path, name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _read_json(name: str) -> Any:
        with open(os.path.join(metadata_path, name), "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_stations() -> None:
        stations = MetadataHandler._get_data("https://rata.digitraffic.fi/api/v1/metadata/stations")

        station_dict = {}

        for s in stations:
            name = s.get("stationName")
            code = s.get("stationShortCode")

            if name and code:
                station_dict[name] = code
                station_dict[code] = name

        MetadataHandler._write_json(station_dict, "station_dict.json")

    @staticmethod
    def load_station_dict() -> Any:
        return MetadataHandler._read_json("station_dict.json")

    @staticmethod
    def save_train_categories():
        train_categories = MetadataHandler._get_data("https://rata.digitraffic.fi/api/v1/metadata/train-categories")

        train_categories_list = [item["name"] for item in train_categories]

        MetadataHandler._write_json(train_categories_list, "train_category_list.json")

    @staticmethod
    def load_train_category_list() -> Any:
        return MetadataHandler._read_json("train_category_list.json")

    @staticmethod
    def save_train_types() -> None:
        train_types = MetadataHandler._get_data("https://rata.digitraffic.fi/api/v1/metadata/train-types")

        train_type_dict = {
            item["name"]: item["trainCategory"]["name"]
            for item in train_types
            if item.get("name") and item.get("trainCategory")
        }

        MetadataHandler._write_json(train_type_dict, "train_types_dict.json")

    @staticmethod
    def load_train_types_dict() -> Any:
        return MetadataHandler._read_json("train_types_dict.json")