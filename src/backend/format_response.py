import json

from typing import List, Optional, Any
from datetime import datetime

from backend.metadata_handler import MetadataHandler

class ResponseFormatter:

    @staticmethod
    def _basic_response_string(train) -> str:
        response_list = []
        response_list.append(f"Train: {train['trainType']} {train['trainNumber']}\n")
        response_list.append(f"Train category: {train['trainCategory']}\n")
        response_list.append(f"Departure date: {train['departureDate']}\n")
        response_list.append(f"Is cancelled: {train['cancelled']}\n")
        # currently at station
        # delayed by
        # from station to station
        return "".join(response_list)

    @staticmethod
    def format_train_status_response(
            train_data,
            only_running_trains: bool = False,
            train_category: Optional[List[str]] = None,
    ):
        response_list = []

        for train in train_data:
            if only_running_trains and not train["runningCurrently"]:
                continue
            elif train_category is not None and train["trainCategory"] not in train_category:
                continue
            else:
                response_list.append(ResponseFormatter._basic_response_string(train))

        return " ".join(response_list)

    @staticmethod
    def _get_departure_and_arrival_time(timetable, departure_station: str, destination_station: str) -> List[Any]:
        response_list = []
        rows = sorted(timetable, key=lambda x: x['scheduledTime'])

        seen = set()
        for r in rows:
            station = r.get("stationShortCode")
            time = r.get("scheduledTime")

            if not station or station in seen:
                continue

            if str(station) == departure_station:
                response_list.append(time)
            elif str(station) == destination_station:
                response_list.append(time)
                break

        return response_list

    @staticmethod
    def _filter_connections(response_list: List[Any], current_time: Any) -> List[Any]:
        filtered_list = []
        for connection in response_list:
            if connection["departure"][1].time() >= current_time:
                filtered_list.append(connection)


        sorted_list = sorted(filtered_list, key=lambda x: x["duration"])
        return sorted_list[:5]

    @staticmethod
    def _turn_connections_into_json_string(
            departure_station: str,
            destination_station: str,
            response_list: List[Any]
    ) -> str:
        station_dict = MetadataHandler.load_station_dict()
        data = {
            "departure_station": station_dict[departure_station],
            "destination_station": station_dict[destination_station],
            "connections_found": True,
            "top_five_connections": []
        }

        if len(response_list) == 0:
            data["connections_found"] = False

        for connection in response_list:
            data["top_five_connections"].append(
                {
                    "train": connection["train_type"] + " " + connection["train_number"],
                    "departure": str(connection["departure"][0]),
                    "arrival": str(connection["arrival"][0]),
                    "duration_minutes": connection["duration"]
                }
            )

        json_string = json.dumps(data, ensure_ascii=False, indent=2)
        return json_string

    @staticmethod
    def format_journey_response(
            train_data,
            departure_station: str,
            destination_station: str,
            current_time: Any
    ) -> str:
        response_list = []

        for train in train_data:
            times = ResponseFormatter._get_departure_and_arrival_time(train['timeTableRows'], departure_station, destination_station)

            departure_time = datetime.fromisoformat(times[0].replace("Z", "+00:00"))
            arrival_time = datetime.fromisoformat(times[1].replace("Z", "+00:00"))
            difference = arrival_time - departure_time

            response_list.append(
                {
                    "train_type": f"{train['trainType']}",
                    "train_number": f"{train['trainNumber']}",
                    "departure": (times[0], departure_time),
                    "arrival": (times[1], arrival_time),
                    "duration": float(difference.total_seconds() / 60)
                }
            )

        response_list = ResponseFormatter._filter_connections(response_list, current_time)

        return ResponseFormatter._turn_connections_into_json_string(
            departure_station,
            destination_station,
            response_list
        )

    @staticmethod
    def _build_timetable_string(timetable):
        rows = sorted(timetable, key=lambda x: x['scheduledTime'])

        seen = set()
        route = []
        for r in rows:
            station = r.get("stationShortCode")

            if not station or station in seen:
                continue

            time = r.get("scheduledTime")

            seen.add(station)

            t = datetime.fromisoformat(time.replace("Z", "+00:00")).strftime("%H:%M")

            station_dict = MetadataHandler.load_station_dict()

            route.append(f"{station_dict.get(station)} {t}")

        route = " → ".join(route)
        route = "Route: " + route

        return route
