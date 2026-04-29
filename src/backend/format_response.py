from typing import List, Optional
from datetime import datetime

from src.backend.metadata_handler import MetadataHandler

def _basic_response_string(train) -> str:
    response_list = []
    response_list.append(f"Train: {train["trainType"]} {train["trainNumber"]}\n")
    response_list.append(f"Train category: {train["trainCategory"]}\n")
    response_list.append(f"Departure date: {train["departureDate"]}\n")
    response_list.append(f"Is cancelled: {train["cancelled"]}\n")
    return "".join(response_list)

def format_train_type_response(
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
            response_list.append(_basic_response_string(train))
            response_list.append("\n")

    return "".join(response_list)

def format_route_response(
        train_data,
        departure_station: str,
        destination_station: str,
) -> str:
    response_list = []

    for train in train_data:
        response_list.append(f""
                             f"{train["trainType"]} "
                             f"{train["trainNumber"]}: "
                             f"{build_route_string(train["timeTableRows"], departure_station, destination_station)}")

    return "\n".join(response_list)

def build_route_string(timetable, departure_station: str, destination_station: str) -> str:
    response_list = []
    rows = sorted(timetable, key=lambda x: x["scheduledTime"])

    seen = set()
    for r in rows:
        station = r.get("stationShortCode")
        time = r.get("scheduledTime")
        time = datetime.fromisoformat(time.replace("Z", "+00:00")).strftime("%H:%M")

        if not station or station in seen:
            continue

        if str(station) == departure_station:
            response_list.append(time)
        elif str(station) == destination_station:
            response_list.append(time)
            break

    return " → ".join(response_list)

def build_timetable_string(timetable):
    rows = sorted(timetable, key=lambda x: x["scheduledTime"])

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
