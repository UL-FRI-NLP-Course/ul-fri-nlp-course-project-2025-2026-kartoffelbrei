from typing import Any, Optional

from llm_engine.router_i import Router
from llm_engine.system_prompts import generate_prompt, PromptType
from llm_engine.model_manager import ModelManager

class AnswerRouter(Router):
    def __init__(self, model_manager: ModelManager):
        self.answer_model = model_manager.answer_model
        self.answer_tokenizer = model_manager.answer_tokenizer

    def extract_answer(self, user_input: str, result: Optional[str] = None) -> Any:
        messages = generate_prompt(prompt_type=PromptType.ANSWER, user_input=user_input, result=result)

        inputs = self.answer_tokenizer.apply_chat_template(
            messages,
            tokenize=True,
            add_generation_prompt=True,
            return_tensors="pt"
        ).to(self.answer_model.device)

        outputs = self.answer_model.generate(
            **inputs,
            max_new_tokens=1000,
            temperature=0.3,
            do_sample=True,
            eos_token_id=self.answer_tokenizer.eos_token_id,
            pad_token_id=self.answer_tokenizer.eos_token_id
        )

        input_length = inputs['input_ids'].shape[1]
        generated = outputs[0][input_length:]

        return self.answer_tokenizer.decode(generated, skip_special_tokens=True)