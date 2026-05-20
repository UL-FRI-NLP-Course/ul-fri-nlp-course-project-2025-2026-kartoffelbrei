import json
from typing import Optional, Any

from llm_engine.router_i import Router
from llm_engine.system_prompts import generate_prompt, PromptType
from llm_engine.model_manager import ModelManager


class IntentRouter(Router):
    def __init__(self, model_manager: ModelManager):
        self.intent_model = model_manager.intent_model
        self.intent_tokenizer = model_manager.intent_tokenizer

    def extract_answer(self, user_input: str, result: Optional[str] = None) -> Any:
        messages = generate_prompt(prompt_type=PromptType.INTENT, user_input=user_input)

        device = self.intent_model.device

        inputs = self.intent_tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(device)

        outputs = self.intent_model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.0,
            do_sample=False,
            eos_token_id=self.intent_tokenizer.eos_token_id,
            pad_token_id=self.intent_tokenizer.eos_token_id,
        )

        input_length = inputs['input_ids'].shape[1]
        generated = outputs[0][input_length:]

        text = self.intent_tokenizer.decode(generated, skip_special_tokens=True)
        print(f"JSON output from intent-router: {text}")
        json_start = text.find("{")
        json_end = text.rfind("}") + 1

        if json_start == -1 or json_end == -1:
            raise ValueError("No JSON found in output")

        json_str = text[json_start:json_end]

        return json.loads(json_str)
