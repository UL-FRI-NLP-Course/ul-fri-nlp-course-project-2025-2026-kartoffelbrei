from dataclasses import dataclass

@dataclass
class ConfigLLM:
    INTENT_MODEL: str = "mistralai/Mistral-7B-Instruct-v0.3"
    ANSWER_MODEL: str = "meta-llama/Llama-3.1-8B-Instruct"
    EMBEDDING_MODEL: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    MODEL_CACHE_DIR: str = "/d/hpc/projects/onj_fri/kartoffelbrei/models" 

