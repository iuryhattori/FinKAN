from src.domain.interfaces.batch_interface import batch_interface   
from src.domain.value_objects.candle_batch import CandleBatch

class BatchCandleRegistry(batch_interface):
    def __init__(self):
        self._batches : list[CandleBatch] = []

    def add(self, batch):
        self._batches.append(batch)

    def latest(self):
        return self._batches[-1] if self._batches else None
    def reset(self):
        self._batches = []  