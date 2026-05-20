
from src.domain.value_objects.raw_data import RawData
import numpy as np

def raw_to_wide_record(
    petr4: np.ndarray,
    wdo: np.ndarray,
    win: np.ndarray,
) -> RawData:
    return RawData(
        DATE=petr4[0],
        PETR4_OPEN=float(petr4[1]),
        PETR4_HIGH=float(petr4[2]),
        PETR4_LOW=float(petr4[3]),
        PETR4_CLOSE=float(petr4[4]),
        PETR4_TICKVOL=float(petr4[5]),
        WDO_OPEN=float(wdo[1]),
        WDO_HIGH=float(wdo[2]),
        WDO_LOW=float(wdo[3]),
        WDO_CLOSE=float(wdo[4]),
        WDO_TICKVOL=float(wdo[5]),
        WIN_OPEN=float(win[1]),
        WIN_HIGH=float(win[2]),
        WIN_LOW=float(win[3]),
        WIN_CLOSE=float(win[4]),
        WIN_TICKVOL=float(win[5]),
    )

def raw_batch_to_wide_records(petr4, wdo, win):
    size = min(len(petr4), len(wdo), len(win))
    result = []
    for i in range(size):
        p = petr4[i]
        w = wdo[i]
        n = win[i]
        record = {
            "DATE": p[0],
            "PETR4_OPEN": float(p[1]),
            "PETR4_HIGH": float(p[2]),
            "PETR4_LOW": float(p[3]),
            "PETR4_CLOSE": float(p[4]),
            "PETR4_TICKVOL": float(p[5]),
            "WDO_OPEN": float(w[1]),
            "WDO_HIGH": float(w[2]),
            "WDO_LOW": float(w[3]),
            "WDO_CLOSE": float(w[4]),
            "WDO_TICKVOL": float(w[5]),
            "WIN_OPEN": float(n[1]),
            "WIN_HIGH": float(n[2]),
            "WIN_LOW": float(n[3]),
            "WIN_CLOSE": float(n[4]),
            "WIN_TICKVOL": float(n[5]),
        }
        result.append(record)
    return result