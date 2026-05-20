from abc import ABC, abstractmethod
from ast import Dict
from typing import Any
from src.domain.entities.Candle import Candle

class DataSource_Interface(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass
    @abstractmethod
    def fetch(self, symbols: str, timeframe : str) -> Dict:
        pass
    @abstractmethod
    def disconnect(self) -> None:
        pass