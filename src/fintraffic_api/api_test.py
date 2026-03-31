import requests


def fetch_live_trains():
    url = "https://rata.digitraffic.fi/api/v1/live-trains"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None


def format_trains(trains):
    results = ""
    for train in trains:
        if train['runningCurrently']:
            train_number = f"{{Train {train['trainNumber']} ({train['trainType']})."
            operator = f"Operator: {train['operatorShortCode']}."
            train_category = f"Train Category: {train['trainCategory']}.}}"
            result = " ".join([train_number, operator, train_category])
            results += result

    return results