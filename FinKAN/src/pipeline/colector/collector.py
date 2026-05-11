
from threading import Lock, Thread
from src.pipeline.meta_trader.inicializer import Mt5
from src.pipeline.abstract.methods import DataSource
from src.pipeline.preprocessing.preprocess import FrameProcessor
import polars as pl


class Collector:
    def __init__(self,
                 symbols : list[str],
                 source : DataSource,
                 process : FrameProcessor):
        self._symbols = symbols
        self._source = source
        self._process = process
        self._active = False
        self._lock   = Lock()
        self._last_df: list[pl.DataFrame] = []

    @property
    def last_df(self) -> pl.DataFrame | None:
        with self._lock:
            return self._last_df
    
    def connect(self) -> None:
        self._source.connect()
        self._active = True

    def stop(self) -> None:
        self._active = False
        self._source.disconnect()

    def collect(self, timeframe : str) -> None:
        while self._active:
            frames = [
                self._source.fetch(symb, timeframe)
                for symb in self._symbols
            ]
            result = self._process.process_data(frames)
            with self._lock:
                self._last_df.append(result)