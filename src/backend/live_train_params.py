from typing import Optional, TypedDict

class LiveTrainParams(TypedDict, total = False):
    arrived_trains: Optional[int]
    arriving_trains: Optional[int]
    departed_trains: Optional[int]
    departing_trains: Optional[int]
    include_nonstopping: Optional[bool]
    train_categories: Optional[str]