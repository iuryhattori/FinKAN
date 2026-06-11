from abc import ABC, abstractmethod
from typing import Any

class PredictorPort(ABC):
    @abstractmethod
    async def predict(self, input: Any) -> Any:
        """Faz predição dos dados processados."""
        pass