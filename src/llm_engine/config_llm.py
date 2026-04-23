# config.py
import os
from dataclasses import dataclass

@dataclass
class ConfigLLM:
    # Modell-Einstellungen
    INTENT_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.3"  # Kleineres Modell für Intent
    ANSWER_MODEL: str = "meta-llama/Llama-3.1-8B-Instruct"     # Größeres für Antworten
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
   