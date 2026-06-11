from typing import TypedDict, Any
from dataclasses import dataclass

@dataclass(frozen=True)
class RawData:
    DATE: str
    PETR4_OPEN: float
    PETR4_HIGH: float
    PETR4_LOW: float
    PETR4_CLOSE: float
    PETR4_TICKVOL: float
    WDO_OPEN: float
    WDO_HIGH: float
    WDO_LOW: float
    WDO_CLOSE: float
    WDO_TICKVOL: float
    WIN_OPEN: float
    WIN_HIGH: float
    WIN_LOW: float
    WIN_CLOSE: float
    WIN_TICKVOL: float