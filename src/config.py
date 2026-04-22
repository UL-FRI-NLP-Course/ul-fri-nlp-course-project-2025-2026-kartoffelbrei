# config.py
import os
from dataclasses import dataclass

@dataclass
class Config:
    # Modell-Einstellungen
    INTENT_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.3"  # Kleineres Modell für Intent
    ANSWER_MODEL: str = "meta-llama/Llama-3.1-8B-Instruct"     # Größeres für Antworten
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    
    # HPC/GPU Einstellungen
    DEVICE_INTENT: str = "cuda:0"  # Erste GPU für Intent-Modell
    DEVICE_ANSWER: str = "cuda:1"  # Zweite GPU für Antwort-Modell (falls verfügbar)
    USE_4BIT: bool = True          # Quantisierung für Speicherersparnis
    
    # Pfade für RAG
    VECTOR_DB_PATH: str = "./data/vector_db"
    SCRAPED_DATA_PATH: str = "./data/bahn_website_texts.json"
    
    # API Konfiguration (Platzhalter für eure echte API)
    API_URL: str = "https://rata.digitraffic.fi/api/v1/"
    #LIVE_TRAINS: str = "https://rata.digitraffic.fi/api/v1/live-trains"
    #GENERAL_TRAIN_INFO: str = "https://rata.digitraffic.fi/api/v1/trains"

config = Config()