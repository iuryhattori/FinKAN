import src.infrastructure.mt5.historical_mt5 as historical_module
from src.infrastructure.mt5.historical_mt5 import HistoricalMt5


def _patch_mt5(monkeypatch, positions_log):
    monkeypatch.setattr(historical_module.mt5, "symbol_select", lambda symbol, enable: True)

    def fake_copy_rates(symbol, timeframe, pos, count):
        positions_log.append(pos)
        return [(1700000000 + pos, 1.0, 2.0, 0.5, 1.5, 100)]

    monkeypatch.setattr(historical_module.mt5, "copy_rates_from_pos", fake_copy_rates)


def test_fetch_replays_history_in_chronological_order(monkeypatch):
    """pos no MT5 conta para o passado: o replay deve decrementar (andar para frente no tempo)."""
    positions = []
    _patch_mt5(monkeypatch, positions)
    source = HistoricalMt5(login=0, password="", server="", start_pos=3)

    for _ in range(4):
        assert source.fetch("PETR4", "M15") is not None

    assert positions == [3, 2, 1, 0]


def test_fetch_stays_on_latest_candle_after_reaching_present(monkeypatch):
    positions = []
    _patch_mt5(monkeypatch, positions)
    source = HistoricalMt5(login=0, password="", server="", start_pos=1)

    for _ in range(4):
        source.fetch("PETR4", "M15")

    assert positions == [1, 0, 0, 0]


def test_fetch_tracks_positions_per_symbol(monkeypatch):
    positions = []
    _patch_mt5(monkeypatch, positions)
    source = HistoricalMt5(login=0, password="", server="", start_pos=2)

    source.fetch("PETR4", "M15")
    source.fetch("WDO$", "M15")
    source.fetch("PETR4", "M15")

    assert positions == [2, 2, 1]
