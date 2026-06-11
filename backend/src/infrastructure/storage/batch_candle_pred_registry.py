from collections import deque

from src.domain.interfaces.batch_registry_interface import BatchRegistryInterface
from src.domain.value_objects.candle_prediction import CandlePrediction

class BatchCandlePredRegistry(BatchRegistryInterface):
    def __init__(self, maxlen: int = 256):
        self._maxlen = maxlen
        self._batches: deque[CandlePrediction] = deque(maxlen=maxlen)

    def add(self, batch):
        self._batches.append(batch)

    def latest(self) -> CandlePrediction:
        return self._batches[-1] if self._batches else None

    def all(self) -> list:
        return list(self._batches)

    def reset(self):
        self._batches = deque(maxlen=self._maxlen)
