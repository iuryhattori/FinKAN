from dataclasses import dataclass
import datetime
import numpy as np
from polars import date



@dataclass(frozen=True)
class Candle:
    symbol : str = ""
    date : datetime = None
    open : float = 0.0
    high : float = 0.0
    low  : float = 0.0
    close: float = 0.0
    tick_vol: int = 0.0

    def __repr__(self):
        return (f"Candle(dt={self.dt}, open={self.open}, high={self.high}, "
                f"low={self.low}, close={self.close}, tick_volume={self.tick_volume})")