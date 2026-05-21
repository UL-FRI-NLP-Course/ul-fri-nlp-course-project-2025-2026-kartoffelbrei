import os

from typing import Union, Dict
from pathlib import Path
from datetime import datetime
from pandas import DataFrame

class FileCreation:
    def __init__(self):
        project_dir = self._find_root()
        result_dir = project_dir / "results"
        time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self._pipeline_log = result_dir / f"pipeline_log_{time}.txt"
        self._metrics = result_dir / f"metrics_{time}.txt"
        self._confusion_matrix = result_dir / f"confusion_matrix_{time}.csv"

    def _find_root(self) -> Path:
        p = Path(__file__).resolve()
        for parent in p.parents:
            if (parent / "ul-fri-nlp-course-project-2025-2026-kartoffelbrei").exists():
                return parent / "ul-fri-nlp-course-project-2025-2026-kartoffelbrei"
        raise RuntimeError("Project root not found")

    def write_pipeline_log(self, log_text: str) -> None:
        with open(os.path.join(Path.cwd(), self._pipeline_log), "a", encoding="utf-8") as f:
            f.write(log_text + "\n")
            print(log_text)

    def write_metrics_file(self, accuracy: float, report: Union[Dict, str]) -> None:
        with open(self._metrics, "w") as f:
            f.write("=== Intent Evaluation Metrics ===\n\n")
            f.write(f"Accuracy: {accuracy:.4f}\n\n")
            f.write("Classification Report:\n")
            f.write(report)

    def write_confusion_matrix_file(self, df: DataFrame ) -> None:
        df.to_csv(self._confusion_matrix)