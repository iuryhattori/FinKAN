import MetaTrader5 as mt5
import pandas as pd
import polars as pl
from datetime import datetime, timezone
import time
from src.pipeline.abstract.methods import DataSource


# Testar adaptação para copy_rates_from (tempo atual) 
class Mt5(DataSource):
    def __init__(self, login : int, password : str, server : str):
        self.login = login
        self.password = password
        self.server = server
    def connect(self) -> None:
        if not mt5.initialize(login= self.login, password = self.password, server = self.server):
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
        return pl.from_pandas(pd.DataFrame(rates_frame))
        
    def disconnect(self) -> None:
        mt5.shutdown()
