from llm_engine.intents import Intent

dataset = [
    # other
    {"text": "What is the weather in Helsinki?", "label": Intent.OTHER.value},
    {"text": "Tell me a joke.", "label": Intent.OTHER.value},
    {"text": "Who won the football match yesterday?", "label": Intent.OTHER.value},
    {"text": "What is the capital of Sweden?", "label": Intent.OTHER.value},
    {"text": "How old is Elon Musk?", "label": Intent.OTHER.value},
    {"text": "What is machine learning?", "label": Intent.OTHER.value},
    {"text": "Play some music.", "label": Intent.OTHER.value},
    # journey search
    {"text": "Can I travel from Helsinki asema to Tampere asema today?", "label": Intent.JOURNEY_SEARCH.value},
    {"text": "What is the next train from Turku asema to Helsinki asema?", "label": Intent.JOURNEY_SEARCH.value},
    {"text": "How do I get from Oulu asema to Rovaniemi?", "label": Intent.JOURNEY_SEARCH.value},
    {"text": "Are there trains from Pasila asema to Lahti this evening?", "label": Intent.JOURNEY_SEARCH.value},
    {"text": "What connections are available between Tampere asema and Turku asema?", "label": Intent.JOURNEY_SEARCH.value},
    {"text": "Can I get from Helsinki asema to Tampere asema after 4pm?", "label": Intent.JOURNEY_SEARCH.value},
    {"text": "Is there a direct train from Vaasa to Seinäjoki?", "label": Intent.JOURNEY_SEARCH.value},
    # station timetable
    {"text": "What trains leave from Helsinki asema today?", "label": Intent.STATION_TIMETABLE.value},
    {"text": "Show departures from Pasila asema.", "label": Intent.STATION_TIMETABLE.value},
    {"text": "What arrivals are expected at Tampere asema?", "label": Intent.STATION_TIMETABLE.value},
    {"text": "Departures from Turku asema after 5pm.", "label": Intent.STATION_TIMETABLE.value},
    {"text": "What trains stop at Tikkurila asema?", "label": Intent.STATION_TIMETABLE.value},
    {"text": "Next departures from Oulu asema.", "label": Intent.STATION_TIMETABLE.value},
    {"text": "What is the station timetable for Lahti?", "label": Intent.STATION_TIMETABLE.value},
    {"text": "Is IC 21 delayed?", "label": Intent.STATION_TIMETABLE.value},
    # train status
    {"text": "Where is S45?", "label": Intent.TRAIN_STATUS.value},
    {"text": "What is the status of Pendolino 51?", "label": Intent.TRAIN_STATUS.value},
    {"text": "Has IC 104 arrived yet?", "label": Intent.TRAIN_STATUS.value},
    {"text": "How late is train IC 22?", "label": Intent.TRAIN_STATUS.value},
    {"text": "Is train PYO 273 running on time?", "label": Intent.TRAIN_STATUS.value},
    {"text": "Where is train S currently?", "label": Intent.TRAIN_STATUS.value},
    {"text": "Is there a direct train from Vaasa to Seinäjoki?", "label": Intent.TRAIN_STATUS.value},
    # general info
    {"text": "Can I bring a bicycle on the train?", "label": Intent.GENERAL_INFO.value},
    {"text": "Are pets allowed on Finnish trains?", "label": Intent.GENERAL_INFO.value},
    {"text": "Do trains have Wi-Fi?", "label": Intent.GENERAL_INFO.value},
    {"text": "Can I buy tickets onboard?", "label": Intent.GENERAL_INFO.value},
    {"text": "What is the refund policy for train tickets?", "label": Intent.GENERAL_INFO.value},
    {"text": "Are there accessible seats available?", "label": Intent.GENERAL_INFO.value},
    {"text": "Can children travel for free?", "label": Intent.GENERAL_INFO.value},
]