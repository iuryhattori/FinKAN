from abc import ABC, abstractmethod
from functools import reduce
import polars as pl

class ProcessorTemplate(ABC):
    @abstractmethod
    def add_prefix(self, lfs: list[pl.LazyFrame]) -> list[pl.LazyFrame]:
        pass

    @staticmethod
    def concat_lfs(lfs: list[pl.LazyFrame], on: str = "DATE") -> pl.LazyFrame:
        return reduce(
            lambda acc, lf: acc.join(lf, on=on, how="full", coalesce=True),
            lfs
        )
    @staticmethod
    def remove_useless_cols(lfs : list[pl.LazyFrame], names : list) -> list[pl.LazyFrame]:
        return [lf.drop(names, strict=True) for lf in lfs]