import requests


def fetch_live_trains():
    url = "https://rata.digitraffic.fi/api/v1/live-trains"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None


def print_trains(trains):
    for train in trains:
        if train['runningCurrently']:
            print(f"Train {train['trainNumber']} ({train['trainType']})")
            print(f"  Operator: {train['operatorShortCode']}")
            print(f"  Train Category: {train['trainCategory']}")
            print()


def run():
    trains = fetch_live_trains()

    if trains:
        print_trains(trains)
    else:
        print("No data available.")