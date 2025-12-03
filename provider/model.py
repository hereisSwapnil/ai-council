# ./provider/model.py

from provider.base import BaseProvider

class Model:
    def __init__(self, name: str, provider_cls: type[BaseProvider]):
        self.name = name
        self.provider = provider_cls(name)

    def generate(self, messages: list[dict[str, str]]):
        return self.provider.generate(messages)
