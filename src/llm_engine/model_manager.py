import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from sentence_transformers import SentenceTransformer
from huggingface_hub import snapshot_download

from src.llm_engine.config_llm import ConfigLLM as Config

class ModelManager:
    def __init__(self):
        self.intent_model = None
        self.intent_tokenizer = None
        self.answer_model = None
        self.answer_tokenizer = None
        self.embedding_model = None
        self.access_token = "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"
        self.local_path = snapshot_download(
            repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            force_download=False,
            max_workers=1
        )
        
    def load_intent_model(self):
        print(f"Load intent-model: {Config.INTENT_MODEL_SMALL}")

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        )
        
        self.intent_tokenizer = AutoTokenizer.from_pretrained(self.local_path, trust_remote_code=True)

        if self.intent_tokenizer.pad_token is None:
            self.intent_tokenizer.pad_token = self.intent_tokenizer.eos_token

        self.intent_tokenizer.padding_side = "left"

        self.intent_model = AutoModelForCausalLM.from_pretrained(
            self.local_path,
            quantization_config=bnb_config,
            device_map="auto",
            torch_dtype=torch.float16,
            trust_remote_code=True,
        )

        self.intent_model.eval()
        self.intent_model.config.use_cache = True
        print("Intent-model loaded")


    def load_answer_model(self):
        print(f"Load answer-model: {Config.ANSWER_MODEL} in {Config.DEVICE_ANSWER}")
        
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=Config.USE_4BIT,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True
        ) if Config.USE_4BIT else None
        
        self.answer_tokenizer = AutoTokenizer.from_pretrained(self.local_path)
        self.answer_model = AutoModelForCausalLM.from_pretrained(
            self.local_path,
            quantization_config=bnb_config,
            device_map=Config.DEVICE_ANSWER,
            torch_dtype=torch.float16
        )
        
    def load_embedding_model(self):
        print(f"Load embedding-model: {Config.EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(self.local_path)
        
    def load_all(self):
        self.load_intent_model()
        #self.load_answer_model()
        #self.load_embedding_model()