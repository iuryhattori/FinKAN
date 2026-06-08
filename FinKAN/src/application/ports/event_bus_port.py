from collections import defaultdict
from abc import ABC, abstractmethod
from typing import Any


class EventBusPort(ABC):
    @abstractmethod
    def subscribe(self, topic: str) -> Any:
        pass

    @abstractmethod
    def unsubscribe(self, topic: str, subscriber: Any) -> None:
        pass

    @abstractmethod
    def publish(self, topic: str, event: Any) -> None:
        pass