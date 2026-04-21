def format_train_type_response(trains):
    for train in trains:
        print(train)
        #train_number = f"{{Train {train['trainNumber']} ({train['trainType']})."
        #operator = f"Operator: {train['operatorShortCode']}."
        #train_category = f"Train Category: {train['trainCategory']}.}}"
        #result = " ".join([train_number, operator, train_category])
        #print(result)
from datetime import datetime

def build_route_string(train_data):
    rows = train_data["timeTableRows"]

    # sort by scheduled time
    rows = sorted(rows, key=lambda x: x["scheduledTime"])

    seen = set()
    route = []

    for r in rows:
        station = r.get("stationShortCode")
        time = r.get("scheduledTime")

        if not station or station in seen:
            continue

        seen.add(station)

        # format time nicely (HH:MM)
        t = datetime.fromisoformat(time.replace("Z", "+00:00")).strftime("%H:%M")

        route.append(f"{station} {t}")

    return " → ".join(route)
