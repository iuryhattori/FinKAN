import logging

from src.domain.interfaces.DataSource_Interface import DataSource_Interface
from src.domain.interfaces.collector_interface import Collector_Interface

logger = logging.getLogger(__name__)

class Collector(Collector_Interface):
    def __init__(self,
                 symbols : list[str],
                 source : DataSource_Interface,):
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
