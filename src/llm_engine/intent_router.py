import json
from typing import Any

from src.llm_engine.system_prompts import intent_prompt_builder
from src.llm_engine.model_manager import ModelManager


class IntentRouter:
    def __init__(self, model_manager: ModelManager):
        self.intent_model = model_manager.intent_model
        self.intent_tokenizer = model_manager.intent_tokenizer

    def extract_intent(self, user_input: str) -> Any:
        prompt = intent_prompt_builder.build(user_input)

        inputs = self.intent_tokenizer(prompt, return_tensors="pt")
        device = self.intent_model.device
        inputs = {k: v.to(device) for k, v in inputs.items()}

        outputs = self.intent_model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.1,
            do_sample=False,
        )

        input_length = inputs["input_ids"].shape[1]
        generated = outputs[0][input_length:]

        text = self.intent_tokenizer.decode(generated, skip_special_tokens=True)

        json_start = text.find("{")
        json_end = text.rfind("}") + 1

        if json_start == -1 or json_end == -1:
            raise ValueError("No JSON found in output")

        json_str = text[json_start:json_end]

        print(json_str)

        return json.loads(json_str)
