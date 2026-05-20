from abc import ABC, abstractmethod
from src.domain.value_objects.raw_data import RawData
from src.domain.entities.Candle import Candle
from typing import Tuple

class DataCollectorPort(ABC):
    @abstractmethod
    async def connect(self) -> None:
        """Inicializa conexão/recursos de coleta."""
        pass

    @abstractmethod
    async def collect_data(self, timeframe: str) -> Tuple[Candle, RawData]:
        """Coleta o próximo Candle + dados brutos para um determinado timeframe."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Libera recursos ou encerra a coleta."""
        pass