from abc import ABC, abstractmethod
import asyncio



class Collector_Interface(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass
    @abstractmethod
    def stop(self) -> None:
        pass
    @abstractmethod
    async def collect(self, timeframe : str) -> None:
        pass