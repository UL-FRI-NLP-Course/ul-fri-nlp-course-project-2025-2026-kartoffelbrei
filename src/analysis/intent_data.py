import pandas as pd

from typing import List, Any
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from llm_engine.intents import Intent

class IntentData:
    def __init__(self, y_pred: List[Any], dataset: List[Any]):
        self.y_pred = y_pred
        self.y_true = self._create_y_true(dataset)

    def _create_y_true(self, dataset: List[Any]) -> List[Any]:
        y_true = []

        for idx, item in enumerate(dataset):
            true_label = item['label']
            y_true.append(true_label)

        return y_true

    def compute_intent_accuracy(self) -> None:
        accuracy = accuracy_score(self.y_true, self.y_pred)
        report = classification_report(self.y_true, self.y_pred)

        with open("metrics.txt", "w") as f:
            f.write("=== Intent Evaluation Metrics ===\n\n")
            f.write(f"Accuracy: {accuracy:.4f}\n\n")
            f.write("Classification Report:\n")
            f.write(report)

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
        df_cm.to_csv("confusion_matrix.csv")