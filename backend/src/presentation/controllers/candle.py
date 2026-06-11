from fastapi import APIRouter, HTTPException, Query, Request
from src.presentation.schemas.candle_schema import CandleHistoryResponse, CandleResponse

candle_router = APIRouter()


def _to_response(candle) -> CandleResponse:
    return CandleResponse(
        symbol=candle.symbol,
        date=float(candle.date) if candle.date is not None else None,
        open=candle.open,
        high=candle.high,
        low=candle.low,
        close=candle.close,
        volume=float(candle.tick_vol),
    )


@candle_router.get("/api/v1/candles/latest", response_model=CandleResponse)
async def get_latest_candle(request: Request):
    app_context = request.app.state.app_context
    batch_candle_registry = app_context["batch_candle_registry"]
    latest_batch = batch_candle_registry.latest()
    if latest_batch is None:
        raise HTTPException(status_code=404, detail="Nenhum candle disponível")
    if not latest_batch.candles:
        raise HTTPException(status_code=404, detail="Nenhum candle disponível")
    return _to_response(latest_batch.candles[-1])


@candle_router.get("/api/v1/candles/history", response_model=CandleHistoryResponse)
async def get_candle_history(request: Request, limit: int = Query(default=100, ge=1, le=1000)):
    """Retorna os últimos N candles coletados, do mais antigo ao mais recente."""
    app_context = request.app.state.app_context
    batch_candle_registry = app_context["batch_candle_registry"]

    candles = [
        candle
        for batch in batch_candle_registry.all()
        for candle in batch.candles
    ]
    return CandleHistoryResponse(candles=[_to_response(c) for c in candles[-limit:]])
