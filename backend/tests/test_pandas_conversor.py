import numpy as np
import pandas as pd

from src.infrastructure.conversors.pandas_conversor import PandasPredictorInputConverter


def test_convert_parses_unix_timestamp_to_utc_datetime():
    converter = PandasPredictorInputConverter()
    records = [
        {"DATE": 1700000000, "PETR4_CLOSE": 35.5},
        {"DATE": 1700000900, "PETR4_CLOSE": 35.7},
    ]
    df = converter.convert(records)

    assert list(df.columns) == ["DATE", "PETR4_CLOSE"]
    assert str(df["DATE"].dt.tz) == "UTC"
    assert df["DATE"].iloc[0] == pd.Timestamp(1700000000, unit="s", tz="UTC")


def test_convert_to_matrix_returns_float32():
    converter = PandasPredictorInputConverter()
    df = pd.DataFrame({"a": [1.0, 2.0], "b": [3.0, 4.0]})
    matrix = converter.convert_to_matrix(df)
    assert matrix.dtype == np.float32
    assert matrix.shape == (2, 2)
