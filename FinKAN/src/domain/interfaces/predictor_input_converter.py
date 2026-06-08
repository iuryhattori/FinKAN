from abc import ABC, abstractmethod
from typing import Any

class PredictorInputConverter(ABC):
    @abstractmethod
    def convert(self, records: list[dict]) -> Any:
        pass
    def convert_to_matrix(self, data : Any) -> Any:
        pass
