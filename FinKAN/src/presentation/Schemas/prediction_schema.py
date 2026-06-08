from pydantic import BaseModel

class PredictionResponse(BaseModel):
    symbol: str
    open: float
    high: float
    low: float
    close: float