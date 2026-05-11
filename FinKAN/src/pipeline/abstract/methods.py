from abc import ABC, abstractmethod
import polars as pl

class DataSource(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass
    @abstractmethod
    def fetch(self, symbols: str, timeframe : str) -> pl.dataframe:
        pass
    @abstractmethod
    def  disconnect(self) -> None:
        pass

class Loader(ABC):
    @abstractmethod
    def load(self) -> list[pl.LazyFrame]:
        pass
    @abstractmethod
    def save(self, lf : pl.LazyFrame, output_folder : str, filename : str) -> None:
        pass