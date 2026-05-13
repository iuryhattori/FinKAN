
from threading import Lock, Thread
from collections import deque
import time
from src.pipeline.meta_trader.Mt5 import Mt5
from src.pipeline.abstract.methods import DataSource
from src.pipeline.preprocessing.preprocess import FrameProcessor
import polars as pl


class Collector:
    def __init__(self,
                 symbols : list[str],
                 source : DataSource,
                 process : FrameProcessor,
                 maxlen : int = 100):
        self._symbols = symbols
        self._source = source
        self._process = process
        self._active = False
        self._lock   = Lock()
        self._last_df: deque[pl.DataFrame] = deque(maxlen=int(maxlen))

    @property
    def last_df(self) -> pl.DataFrame | None:
        with self._lock:
            return self._last_df[-1] if self._last_df else None
    
    def connect(self) -> None:
        self._source.connect()
        self._active = True

    def stop(self) -> None:
        self._active = False
        try:
            self._source.disconnect()
        except Exception as e:
            print()

    def collect(self, timeframe : str, interval : float = 5.0) -> None:
        while self._active:
            frames = [
                self._source.fetch(symb, timeframe)
                for symb in self._symbols
            ]
            result = self._process.process_data(frames)
            with self._lock:
                self._last_df.append(result)
                print(self._last_df[-1])
                
            time.sleep(interval)