from pydantic import BaseModel

class CandleResponse(BaseModel):
    open: float
    high: float
    low: float
    close: float