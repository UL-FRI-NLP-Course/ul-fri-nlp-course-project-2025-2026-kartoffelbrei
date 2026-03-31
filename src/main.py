from fintraffic_api.api_test import fetch_live_trains, format_trains
from llm_engine.llm_test import run_llm

if __name__ == "__main__":
    trains = format_trains(fetch_live_trains())
    run_llm(trains)