from abc import ABC, abstractmethod
from typing import Any


class EventPublisherPort(ABC):
    @abstractmethod
    def publish(self, topic: str, event: Any) -> None:
        pass