
from os import rename
from threading import Lock, Thread
from collections import deque
import traceback
import numpy as np
import time
import pandas as pd
from src.domain.interfaces.DataSource_Interface import DataSource_Interface
from src.domain.entities.Candle import Candle
from src.domain.interfaces.collector_interface import Collector_Interface
import asyncio
import polars as pl

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
            print(f"[ERROR] {type(e).__name__}: {e}")
            traceback.print_exc()

    async def collect(self, timeframe : str) -> None:
            candles = {}
            for symbol in self._symbols:
                data = self._source.fetch(symbol, timeframe)
                candles[symbol] = data
            return candles
            
            

            
            
            
    
