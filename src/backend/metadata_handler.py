import os.path
import requests
import json
from typing import Any
from pathlib import Path

class MetadataHandler:
    base_dir = Path(__file__).resolve().parent
    metadata_path: str = os.path.join(base_dir.parent, "metadata")

    def _get_data(self, url: str) -> Any:
        return requests.get(url).json()

    def _write_json(self, data: Any, name: str) -> None:
        with open(os.path.join(self.metadata_path, name), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _read_json(self, name: str) -> Any:
        with open(os.path.join(self.metadata_path, name), "r", encoding="utf-8") as f:
            return json.load(f)

    def save_stations(self) -> None:
        stations = self._get_data("https://rata.digitraffic.fi/api/v1/metadata/stations")

        station_dict = {
            s["stationName"]: s["stationShortCode"]
            for s in stations
            if s.get("stationShortCode") and s.get("stationName")
        }

        self._write_json(station_dict, "station_dict.json")

    def load_station_dict(self) -> Any:
        return self._read_json("station_dict.json")

    def save_train_categories(self):
        train_categories = self._get_data("https://rata.digitraffic.fi/api/v1/metadata/train-categories")

        train_categories_list = [item["name"] for item in train_categories]

        self._write_json(train_categories_list, "train_category_list.json")

    def load_train_category_list(self) -> Any:
        return self._read_json("train_category_list.json")

    def save_train_types(self) -> None:
        train_types = self._get_data("https://rata.digitraffic.fi/api/v1/metadata/train-types")

        train_type_dict = {
            item["name"]: item["trainCategory"]["name"]
            for item in train_types
            if item.get("name") and item.get("trainCategory")
        }

        self._write_json(train_type_dict, "train_types_dict.json")

    def load_train_types_dict(self) -> Any:
        return self._read_json("train_types_dict.json")