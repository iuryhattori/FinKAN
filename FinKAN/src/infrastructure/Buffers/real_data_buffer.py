from src.domain.interfaces.buffer_interface import BufferInterface
from src.domain.value_objects.raw_data import RawData
import numpy as np
import pandas as pd



class RealDataBuffer(BufferInterface):
    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.data : list[RawData] = []

    def add(self, data : RawData):
        self.data.append(data)

    @property
    def size(self) -> int:
        return len(self.data)
    @property
    def is_full(self) -> bool:
        return self.size == self.batch_size
        
    def reset(self) -> None:
        self.data.clear()