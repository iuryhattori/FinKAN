from collections import deque

from src.domain.interfaces.batch_interface import batch_interface

class BatchPredRegistry(batch_interface):
    def __init__(self, maxlen: int = 256):
        self._maxlen = maxlen
        self._batches = deque(maxlen=maxlen)

    def add(self, batch):
        self._batches.append(batch)

    def latest(self):
        return self._batches[-1] if self._batches else None

    def reset(self):
        self._batches = deque(maxlen=self._maxlen)
