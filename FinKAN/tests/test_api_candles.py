import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.domain.value_objects.candle import Candle
from src.domain.value_objects.candle_batch import CandleBatch
from src.infrastructure.storage.batch_candle_registry import BatchCandleRegistry
from src.presentation.controllers.candle import candle_router


def _candle(close: float, date: float = 1700000000.0) -> Candle:
    return Candle(
        symbol="PETR4",
        date=date,
        open=close - 0.2,
        high=close + 0.3,
        low=close - 0.4,
        close=close,
        tick_vol=1500,
    )


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(candle_router)
    registry = BatchCandleRegistry()
    app.state.app_context = {"batch_candle_registry": registry}
    return TestClient(app), registry


def test_latest_candle_returns_404_when_empty(client):
    test_client, _ = client
    response = test_client.get("/api/v1/candles/latest")
    assert response.status_code == 404


def test_latest_candle_returns_full_contract(client):
    test_client, registry = client
    registry.add(CandleBatch(candles=[_candle(35.0), _candle(35.5)], batch_id=0))

    response = test_client.get("/api/v1/candles/latest")

    assert response.status_code == 200
    body = response.json()
    assert body == {
        "symbol": "PETR4",
        "date": 1700000000.0,
        "open": 35.3,
        "high": 35.8,
        "low": 35.1,
        "close": 35.5,
        "volume": 1500.0,
    }


def test_history_returns_empty_list_when_no_data(client):
    test_client, _ = client
    response = test_client.get("/api/v1/candles/history")
    assert response.status_code == 200
    assert response.json() == {"candles": []}


def test_history_flattens_batches_and_applies_limit(client):
    test_client, registry = client
    registry.add(CandleBatch(candles=[_candle(35.0), _candle(35.1)], batch_id=0))
    registry.add(CandleBatch(candles=[_candle(35.2), _candle(35.3)], batch_id=1))

    response = test_client.get("/api/v1/candles/history?limit=3")

    assert response.status_code == 200
    closes = [c["close"] for c in response.json()["candles"]]
    assert closes == [35.1, 35.2, 35.3]


def test_history_rejects_invalid_limit(client):
    test_client, _ = client
    assert test_client.get("/api/v1/candles/history?limit=0").status_code == 422
