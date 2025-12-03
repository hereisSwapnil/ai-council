# ./provider/base.py

from abc import ABC, abstractmethod

class BaseProvider(ABC):
    def __init__(self, model: str):
        self.model = model
    
    @abstractmethod
    def generate(self, messages: list[dict[str, str]]):
        raise NotImplementedError