import logging

from src.domain.interfaces.data_source_interface import DataSourceInterface
from src.domain.interfaces.collector_interface import CollectorInterface

logger = logging.getLogger(__name__)

class Collector(CollectorInterface):
    def __init__(self,
                 symbols : list[str],
                 source : DataSourceInterface,):
        self._symbols = symbols
        self._source = source

    def connect(self) -> None:
        self._source.connect()

    def stop(self) -> None:
        try:
            self._source.disconnect()
        except Exception as e:
            logger.exception(f"Erro ao desconectar source: {type(e).__name__}: {e}")

    async def collect(self, timeframe : str) -> dict:
        candles = {}
        for symbol in self._symbols:
            data = self._source.fetch(symbol, timeframe)
            candles[symbol] = data
        return candles
