from abc import ABC, abstractmethod
from src.domain.value_objects.raw_data import RawData
import numpy as np


class BufferInterface(ABC):
    @abstractmethod
    def add(self, data : RawData)-> None:
        pass
    @abstractmethod
    def is_full(self) -> bool:
        pass
    @abstractmethod
    def size(self) -> int:
        pass
    @abstractmethod
    def reset(self) -> None:
        pass