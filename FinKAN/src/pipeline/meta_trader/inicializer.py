import MetaTrader5 as mt5
import polars as pl
import time
from src.pipeline.abstract.methods import DataSource

class Mt5(DataSource):
    def connect(self) -> None:
        if not mt5.initialize():
            raise ConnectionError(f"MT5 init failed: {mt5.last_error()}")

    def fetch(self, symbol : str, timeframe : str):
        date = time.time()
        raw = mt5.copy_rates_from(symbol, timeframe, date, 1)
        if raw is None:
            raise ValueError(f"No data for {symbol}: {mt5.last_error()}")
        
    def disconnect(self) -> None:
        mt5.shutdown()
