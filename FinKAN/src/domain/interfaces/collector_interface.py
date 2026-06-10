from abc import ABC, abstractmethod


class CollectorInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass
    @abstractmethod
    def stop(self) -> None:
        pass
    @abstractmethod
    async def collect(self, timeframe : str) -> None:
        pass