import os

from typing import Optional
from pathlib import Path
from enum import Enum, auto

from llm_prompts.intent_prompt import intent_prompt
from llm_prompts.answer_prompt import answer_prompt

class PromptType(Enum):
    ANSWER = auto()
    INTENT = auto()

def load_prompt(path):
    return Path(path).read_text()

def generate_prompt(prompt_type: PromptType, user_input: str, result: Optional[str] = None) ->  list[dict[str, str]]:
    #BASE_DIR = Path(__file__).resolve().parent.parent
    #print(BASE_DIR) # Datei, in der dieser Code steht
    #path = os.path.join(BASE_DIR, "llm_prompts")
    

    system_prompt = ""
    user_prompt = ""
    match prompt_type:
        case PromptType.ANSWER:
            system_prompt = answer_prompt#load_prompt(os.path.join(path, "answer_prompt.txt"))
            user_prompt = f"""
            User question: 
                {user_input}

            Retrieved context: {result}

            Generate the best possible answer.
            """
        case PromptType.INTENT:
            system_prompt = intent_prompt #load_prompt(path / "intent_prompt.txt")
            user_prompt = user_input

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    return messages
