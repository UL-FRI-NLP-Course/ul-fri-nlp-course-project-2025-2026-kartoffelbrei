import os

from typing import Optional
from pathlib import Path
from enum import Enum, auto

class PromptType(Enum):
    ANSWER = auto()
    INTENT = auto()

def load_prompt(path):
    return Path(path).read_text()

def generate_prompt(prompt_type: PromptType, user_input: str, result: Optional[str] = None) ->  list[dict[str, str]]:
    path = os.path.join("src", "llm_prompts")

    system_prompt = ""
    user_prompt = ""
    match prompt_type:
        case PromptType.ANSWER:
            system_prompt = load_prompt(os.path.join(path, "answer_prompt.txt"))
            user_prompt = f"""
            User question: 
{user_input}

Retrieved context: {result}

Generate the best possible answer.
"""
        case PromptType.INTENT:
            system_prompt = load_prompt(os.path.join(path, "intent_prompt.txt"))
            user_prompt = user_input

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    print(f"PromptType: {prompt_type.name}, \n Message: {messages}")

    return messages
