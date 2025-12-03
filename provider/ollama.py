# ./provider/ollama.py

import requests
from provider.base import BaseProvider

class Ollama(BaseProvider):
    def __init__(self, model: str):
        super().__init__(model)
    
    def generate(self, messages: list[dict[str, str]]):
        url = "http://localhost:11434/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        res = requests.post(url, json=payload)
        return res.json()