import pytest

from src.infrastructure.adapters.data_collector_adapter import DataCollectorAdapter


class FakeCollector:
    def __init__(self, candles):
        self._candles = candles
        self.connected = False
        self.stopped = False

    def connect(self):
        self.connected = True

    def stop(self):
        self.stopped = True

    async def collect(self, timeframe):
        return self._candles


def _record(date=1700000000, base=10.0):
    return (date, base, base + 1, base - 1, base + 0.5, 100)


def _full_candles():
    return {
        "PETR4": _record(base=35.0),
        "WDO$": _record(base=5000.0),
        "WIN$": _record(base=120000.0),
    }


async def test_collect_data_returns_candle_and_raw_data():
    adapter = DataCollectorAdapter(FakeCollector(_full_candles()))
    candle, raw = await adapter.collect_data("M15")

    assert candle.symbol == "PETR4"
    assert candle.open == 35.0
    assert candle.close == 35.5
    assert raw.PETR4_OPEN == 35.0
    assert raw.WDO_CLOSE == 5000.5
    assert raw.WIN_HIGH == 120001.0


async def test_collect_data_raises_when_target_symbol_missing():
    candles = _full_candles()
    candles.pop("PETR4")
    adapter = DataCollectorAdapter(FakeCollector(candles))

    with pytest.raises(ValueError, match="PETR4"):
        await adapter.collect_data("M15")


async def test_collect_data_raises_when_symbol_data_is_none():
    candles = _full_candles()
    candles["WIN$"] = None
    adapter = DataCollectorAdapter(FakeCollector(candles))

    with pytest.raises(ValueError, match="WIN"):
        await adapter.collect_data("M15")


async def test_connect_and_stop_dispatch_sync_collector():
    collector = FakeCollector(_full_candles())
    adapter = DataCollectorAdapter(collector)

    await adapter.connect()
    await adapter.stop()
    assert collector.connected
    assert collector.stopped
