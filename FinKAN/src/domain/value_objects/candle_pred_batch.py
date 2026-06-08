from dataclasses import dataclass
from src.domain.value_objects.candle_prediction import CandlePrediction
from typing import List

@dataclass(frozen=True)
class CandlePredBatch:
    predictions: List[CandlePrediction]
    batch_id: int