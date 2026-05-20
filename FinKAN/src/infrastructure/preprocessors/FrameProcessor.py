import os
from pathlib import Path
import polars as pl
import numpy as np
from src.infrastructure.templates.ProcessorTemplate import ProcessorTemplate
import datetime as datetime


class FrameProcessor(ProcessorTemplate):
    def __init__(self, names : list[str]) -> None:
        self._names = names

    def load(self, frames: list[np.ndarray]) -> list[pl.LazyFrame]:
        return [pl.DataFrame(df).lazy() for df in frames]
    
    def add_prefix(self, lfs : list[pl.LazyFrame]) -> list[pl.LazyFrame]:
        return [
            lf.rename({
                col : f"{name}_{col}"
                for col in lf.collect_schema().names()
                if col != "time"
            })
            for lf, name in zip(lfs, self._names)
        ]
    def process_data(self, frames : list[np.ndarray]):
        lfs = self.load(frames)
        lfs = self.remove_useless_cols(lfs, ["spread", "real_volume"])
        lfs = self.add_prefix(lfs)
        lf = self.concat_lfs(lfs, "time")
        return lf.collect()