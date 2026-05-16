from typing import Optional, Any
from abc import ABC, abstractmethod

from llm_engine.model_manager import ModelManager

class Router(ABC):
    @abstractmethod
    def __init__(self, model_manager: ModelManager):
        ...

    @abstractmethod
    def extract_answer(self, user_input: str, result: Optional[str] = None) -> Any:
        ...