import pandas as pd

from typing import List, Any
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from llm_engine.intents import Intent
from util.file_creation import FileCreation

class IntentData:
    def __init__(self, y_pred: List[Any], dataset: List[Any], file_creation: FileCreation):
        self.y_pred = y_pred
        self.y_true = self._create_y_true(dataset)
        self.file_creation = file_creation

    def _create_y_true(self, dataset: List[Any]) -> List[Any]:
        y_true = []

        for idx, item in enumerate(dataset):
            true_label = item['label']
            y_true.append(true_label)

        return y_true

    def compute_intent_accuracy(self) -> None:
        accuracy = accuracy_score(self.y_true, self.y_pred)
        report = classification_report(self.y_true, self.y_pred)

        self.file_creation.write_metrics_file(accuracy=accuracy, report=report)

    def compute_confusion_matrix(self) -> None:
        labels = [
            Intent.JOURNEY_SEARCH.value,
            Intent.STATION_TIMETABLE.value,
            Intent.TRAIN_STATUS.value,
            Intent.GENERAL_INFO.value,
            Intent.OTHER.value
        ]

        cm = confusion_matrix(self.y_true, self.y_pred, labels=labels)

        df_cm = pd.DataFrame(cm, index=labels, columns=labels)
        self.file_creation.write_confusion_matrix_file(df=df_cm)