
from abc import ABC, abstractmethod
from typing import Any

class BatchRegistryInterface(ABC):
    @abstractmethod
    def add(self, data):
        pass
    @abstractmethod
    def reset(self) -> None:
        pass
    @abstractmethod
    def latest(self) -> Any:
        """Retorna o elemento mais recente (candle ou batch)."""
        pass
    @abstractmethod
    def all(self) -> list:
        """Retorna todos os elementos retidos, do mais antigo ao mais recente."""
        pass
