# ./provider/open_router.py

import requests
from provider.base import BaseProvider
import os
from dotenv import load_dotenv

load_dotenv()

class OpenRouter(BaseProvider):
    def __init__(self, model: str):
        super().__init__(model)
        self.api_key = os.getenv("OPENROUTER_API_KEY")

    def generate(self, messages: list[dict[str, str]]):
        url = "https://openrouter.ai/api/v1/chat/completions"
        payload = {
            "model": self.model,
            "messages": messages
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        res = requests.post(url, json=payload, headers=headers)
        return res.json()
