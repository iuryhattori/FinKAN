
from abc import ABC, abstractmethod
from typing import Any

class batch_interface(ABC):
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