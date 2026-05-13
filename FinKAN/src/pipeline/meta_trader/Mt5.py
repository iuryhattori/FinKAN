import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timezone
import time
from src.pipeline.abstract.methods import DataSource

class Mt5(DataSource):
    def connect(self) -> None:
        if not mt5.initialize():
            raise ConnectionError(f"MT5 init failed: {mt5.last_error()}")

    def fetch(self, symbol : str, timeframe):
        if not mt5.symbol_select(symbol, True):
            print(f"[MT5] Símbolo '{symbol}' não encontrado no broker")
            return None
        date = datetime.now(timezone.utc)
        raw = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1)
        if raw is None:
            code, msg = mt5.last_error()
            print(f"[MT5 fetch error] symbol='{symbol}' [{code}]: {msg}")
            return None
        rates_frame = pd.DataFrame(raw)
        rates_frame["time"] = pd.to_datetime(rates_frame['time'], unit='s')

        return rates_frame
        
    def disconnect(self) -> None:
        mt5.shutdown()
