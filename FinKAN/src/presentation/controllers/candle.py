from fastapi import APIRouter, HTTPException, Request
import asyncio
from src.presentation.schemas.candle_schema import CandleResponse

candle_router = APIRouter()

@candle_router.get("/api/v1/candles/latest", response_model=CandleResponse)
async def get_latest_candle(request: Request):
    app_context = request.app.state.app_context
    batch_candle_registry = app_context["batch_candle_registry"]
    latest_batch = batch_candle_registry.latest()
    if latest_batch is None:
        raise HTTPException(status_code=404, detail="Nenhum candle disponível")
    if not latest_batch.candles:
        raise HTTPException(status_code=404, detail="Nenhum candle disponível")
    latest_candle = latest_batch.candles[-1]
    return CandleResponse(
        open=latest_candle.open,
        high=latest_candle.high,
        low=latest_candle.low,
        close=latest_candle.close,
    )