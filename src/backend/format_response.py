from typing import List
from datetime import datetime

from .metadata_handler import MetadataHandler

def format_train_type_response(train_data, only_running_trains: bool = False, train_category: List[str] = None):
    response_list = []

    for train in train_data:
        if only_running_trains and not train["runningCurrently"]:
            continue
        elif train_category is not None and train["trainCategory"] not in train_category:
            continue
        else:
            response_list.append(f"Train: {train["trainType"]} {train["trainNumber"]}\n")
            response_list.append(f"Train category: {train["trainCategory"]}\n")
            response_list.append(f"Departure date: {train["departureDate"]}\n")
            response_list.append(f"Is currently running: {train["runningCurrently"]}\n")
            response_list.append(f"Is cancelled: {train["cancelled"]}\n")
            response_list.append(build_timetable_string(train["timeTableRows"]) + "\n")
            response_list.append("\n")

    return "".join(response_list)


def build_timetable_string(timetable):
    rows = sorted(timetable, key=lambda x: x["scheduledTime"])

    seen = set()
    route = []
    for r in rows:
        station = r.get("stationShortCode")
        time = r.get("scheduledTime")

        if not station or station in seen:
            continue

        seen.add(station)

        t = datetime.fromisoformat(time.replace("Z", "+00:00")).strftime("%H:%M")

        station_dict = MetadataHandler.load_station_dict()

        route.append(f"{station_dict.get(station)} {t}")

    route = " → ".join(route)
    route = "Route: " + route

    return route
