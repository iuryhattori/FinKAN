from pydantic import BaseModel

class CandleResponse(BaseModel):
    symbol: str = ""
    date: float | None = None
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0


class CandleHistoryResponse(BaseModel):
    candles: list[CandleResponse]
