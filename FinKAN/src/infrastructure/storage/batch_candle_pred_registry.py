from src.domain.interfaces.batch_interface import batch_interface   
from src.domain.value_objects.candle_pred_batch import CandlePredBatch
from src.domain.value_objects.candle_prediction import CandlePrediction

class BatchCandlePredRegistry(batch_interface):
    def __init__(self):
        self._batches : list[CandlePredBatch] = []

    def add(self, batch):
        self._batches.append(batch)

    def latest(self) -> CandlePrediction:
        return self._batches[-1] if self._batches else None
    def reset(self):
        self._batches = []  