from src.domain.value_objects.raw_data import RawData

# Mapeia o símbolo do broker para o prefixo das features esperado pelo modelo.
# A ordem das chaves define a ordem das colunas do dataset de treino.
DEFAULT_SYMBOL_PREFIXES: dict[str, str] = {
    "PETR4": "PETR4",
    "WDO$": "WDO",
    "WIN$": "WIN",
}

# Layout posicional dos registros retornados pelo MT5 (copy_rates_from_pos).
_OHLCV_FIELDS = ("OPEN", "HIGH", "LOW", "CLOSE", "TICKVOL")


def records_to_raw_data(
    records: dict,
    symbol_prefixes: dict[str, str] = DEFAULT_SYMBOL_PREFIXES,
) -> RawData:
    """Converte os registros coletados por símbolo em um RawData wide."""
    missing = [s for s in symbol_prefixes if records.get(s) is None]
    if missing:
        raise ValueError(
            f"Dados ausentes para os símbolos {missing}. "
            f"Símbolos coletados: {list(records.keys())}"
        )

    first_symbol = next(iter(symbol_prefixes))
    kwargs = {"DATE": records[first_symbol][0]}
    for symbol, prefix in symbol_prefixes.items():
        record = records[symbol]
        for offset, field in enumerate(_OHLCV_FIELDS, start=1):
            kwargs[f"{prefix}_{field}"] = float(record[offset])
    return RawData(**kwargs)


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
