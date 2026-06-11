from abc import ABC, abstractmethod
from typing import Any

class DataSourceInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass
    @abstractmethod
    def fetch(self, symbols: str, timeframe : str) -> Any:
        pass
    @abstractmethod
    def disconnect(self) -> None:
        pass