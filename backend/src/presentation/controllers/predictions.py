from fastapi import APIRouter, HTTPException, Request

from src.presentation.schemas.prediction_schema import PredictionResponse

router = APIRouter()



@router.get("/api/v1/predictions/latest", response_model=PredictionResponse)
async def get_latest_prediction(request: Request):
    """Endpoint para obter a última predição."""
    app_context = request.app.state.app_context
    batch_candle_pred_registry = app_context["batch_candle_pred_registry"]
    latest_prediction = batch_candle_pred_registry.latest()
    
    if latest_prediction is None:
        raise HTTPException(status_code=404, detail="Nenhuma predição disponível")
    
    return PredictionResponse(
        symbol=latest_prediction.symbol,
        open=latest_prediction.open,
        high=latest_prediction.high,
        low=latest_prediction.low,
        close=latest_prediction.close,
    )