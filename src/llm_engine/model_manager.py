import torch
from typing import Union, List
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from sentence_transformers import SentenceTransformer
from huggingface_hub import snapshot_download, DryRunFileInfo

from .config_llm import ConfigLLM as Config

class ModelManager:
    def __init__(self):
        self.intent_model = None
        self.intent_tokenizer = None
        self.answer_model = None
        self.answer_tokenizer = None
        self.embedding_model = None

    @staticmethod
    def _download_model(repo_id: str) -> Union[str, List[DryRunFileInfo]]:
        return snapshot_download(
            repo_id=repo_id,
            force_download=False,
            max_workers=1
        )
        
    def load_intent_model(self):
        print(f"Load intent-model: {Config.INTENT_MODEL}")

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )

        local_path = self._download_model(Config.INTENT_MODEL)
        
        self.intent_tokenizer = AutoTokenizer.from_pretrained(local_path, trust_remote_code=True)

        if self.intent_tokenizer.pad_token is None:
            self.intent_tokenizer.pad_token = self.intent_tokenizer.eos_token

        self.intent_tokenizer.padding_side = "left"

        self.intent_model = AutoModelForCausalLM.from_pretrained(
            local_path,
            quantization_config=bnb_config,
            device_map="auto",
            dtype=torch.float16,
            trust_remote_code=True,
        )

        self.intent_model.eval()
        self.intent_model.config.use_cache = True
        print("Intent-model loaded")

    def load_answer_model(self):
        print(f"Load answer-model: {Config.ANSWER_MODEL}")

        local_path = self._download_model(Config.ANSWER_MODEL)

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )

        self.answer_tokenizer = AutoTokenizer.from_pretrained(
            local_path,
            use_fast=True
        )

        if self.answer_tokenizer.pad_token is None:
            self.answer_tokenizer.pad_token = self.answer_tokenizer.eos_token

        self.answer_tokenizer.padding_side = "left"

        self.answer_model = AutoModelForCausalLM.from_pretrained(
            local_path,
            quantization_config=bnb_config,
            torch_dtype=torch.float16,
            device_map="auto"
        )

        self.answer_model.eval()
        print("Answer model loaded")
        
    def load_embedding_model(self):
        print(f"Load embedding-model: {Config.EMBEDDING_MODEL}")

        local_path = self._download_model(Config.EMBEDDING_MODEL)

        self.embedding_model = SentenceTransformer(local_path)
        
    def load_all(self):
        self.load_intent_model()
        self.load_answer_model()
        #self.load_embedding_model()