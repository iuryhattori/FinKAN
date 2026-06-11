import pytest

from src.application.helpers.helper import records_to_raw_data, DEFAULT_SYMBOL_PREFIXES


def _record(date=1700000000, base=10.0):
    # Layout posicional do MT5: (time, open, high, low, close, tick_volume)
    return (date, base, base + 1, base - 1, base + 0.5, 100)


def test_records_to_raw_data_maps_all_symbols():
    records = {
        "PETR4": _record(base=35.0),
        "WDO$": _record(base=5000.0),
        "WIN$": _record(base=120000.0),
    }
    raw = records_to_raw_data(records)

    assert raw.DATE == 1700000000
    assert raw.PETR4_OPEN == 35.0
    assert raw.PETR4_CLOSE == 35.5
    assert raw.WDO_HIGH == 5001.0
    assert raw.WIN_LOW == 119999.0
    assert raw.WIN_TICKVOL == 100.0


def test_records_to_raw_data_raises_on_missing_symbol():
    records = {"PETR4": _record()}
    with pytest.raises(ValueError, match="WDO"):
        records_to_raw_data(records)


def test_records_to_raw_data_raises_on_none_data():
    records = {
        "PETR4": _record(),
        "WDO$": None,
        "WIN$": _record(),
    }
    with pytest.raises(ValueError, match="WDO"):
        records_to_raw_data(records)


def test_default_prefixes_cover_expected_symbols():
    assert list(DEFAULT_SYMBOL_PREFIXES.keys()) == ["PETR4", "WDO$", "WIN$"]
