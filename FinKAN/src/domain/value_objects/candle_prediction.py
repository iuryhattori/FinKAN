from dataclasses import dataclass

@dataclass(frozen=True)
class CandlePrediction:
    symbol: str
    raw_data: float

    @property
    def open(self):
        return self.raw_data[0,-1, 0]
    @property
    def high(self):
        return self.raw_data[0, -1, 1]
    @property
    def low(self):
        return self.raw_data[0, -1, 2]
    @property
    def close(self):
        return self.raw_data[0, -1, 3]
