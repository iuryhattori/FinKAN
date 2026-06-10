from dataclasses import dataclass
from typing import List
from src.domain.value_objects.candle import Candle

@dataclass(frozen=True)
class CandleBatch:
    candles: List[Candle]
    batch_id: int
