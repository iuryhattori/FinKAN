import asyncio
import json
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

sse_router = APIRouter()

@sse_router.get("/api/v1/stream")
async def stream_market(request: Request):
    app_context = request.app.state.app_context

    async def event_generator():
        last_seen = None

        while True:
            try:
                if await request.is_disconnected():
                    print("Cliente desconectado do stream")
                    break

                candle_reg = app_context["batch_candle_registry"]
                pred_reg = app_context["batch_candle_pred_registry"]

                latest_batch = candle_reg.latest()
                latest_pred = pred_reg.latest()

                if latest_batch and latest_batch.candles:
                    candle = latest_batch.candles[-1]

                    pred_payload = None
                    if latest_pred is not None:
                        pred_payload = {
                            "symbol": latest_pred.symbol,
                            "open": latest_pred.open,
                            "high": latest_pred.high,
                            "low": latest_pred.low,
                            "close": latest_pred.close,
                        }

                    current_key = (
                        candle.open, candle.high, candle.low, candle.close,
                        pred_payload["open"] if pred_payload else None,
                        pred_payload["high"] if pred_payload else None,
                        pred_payload["low"] if pred_payload else None,
                        pred_payload["close"] if pred_payload else None,
                    )

                    if current_key != last_seen:
                        last_seen = current_key

                        payload = {
                            "candle": {
                                "open": candle.open,
                                "high": candle.high,
                                "low": candle.low,
                                "close": candle.close,
                            },
                            "pred": pred_payload,
                        }

                        yield f"data: {json.dumps(payload)}\n\n"

                await asyncio.sleep(1)

            except Exception as e:
                print("Erro no event_generator:", repr(e))
                await asyncio.sleep(1)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )