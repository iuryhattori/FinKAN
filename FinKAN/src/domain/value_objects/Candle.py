from dataclasses import dataclass
import datetime


@dataclass(frozen=True)
class Candle:
    symbol : str = ""
    date : datetime.datetime = None
    open : float = 0.0
    high : float = 0.0
    low  : float = 0.0
    close: float = 0.0
    tick_vol: float = 0.0

    def __repr__(self):
        return (f"Candle(symbol={self.symbol}, date={self.date}, open={self.open}, "
                f"high={self.high}, low={self.low}, close={self.close}, "
                f"tick_vol={self.tick_vol})")
