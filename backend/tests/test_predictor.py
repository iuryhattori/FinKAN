import joblib
import numpy as np
import pandas as pd
import pytest
from sklearn.preprocessing import RobustScaler

from src.infrastructure.config.predictor_settings import PredictorSettings
from src.infrastructure.predictor.predictor import Predictor

N_FEATURES = 15
SEQ_LEN = 4
PRED_LEN = 4
N_TARGETS = 4


class FakeOnnxSession:
    def __init__(self, output: np.ndarray):
        self.output = output
        self.last_inputs = None

    def run(self, output_names, inputs):
        self.last_inputs = inputs
        return [self.output]


@pytest.fixture
def scalers_path(tmp_path):
    rng = np.random.default_rng(42)
    scaler = RobustScaler().fit(rng.normal(size=(50, N_FEATURES)))
    joblib.dump(scaler, tmp_path / Predictor.SCALER_FILENAME)
    return tmp_path


@pytest.fixture
def settings(scalers_path):
    return PredictorSettings(
        seq_len=SEQ_LEN,
        pred_len=PRED_LEN,
        n_targets=N_TARGETS,
        scale=True,
        scalers_path=str(scalers_path),
    )


@pytest.fixture
def input_df():
    rng = np.random.default_rng(7)
    df = pd.DataFrame(
        {"DATE": pd.date_range("2026-01-05 10:00", periods=SEQ_LEN, freq="15min", tz="UTC")}
    )
    for i in range(N_FEATURES):
        df[f"F{i}"] = rng.normal(size=SEQ_LEN)
    return df


async def test_predict_returns_denormalized_targets(settings, input_df):
    model_output = np.ones((1, PRED_LEN, N_FEATURES), dtype=np.float32)
    session = FakeOnnxSession(model_output)
    predictor = Predictor(session, settings)

    result = await predictor.predict(input_df)

    assert result.shape == (1, PRED_LEN, N_TARGETS)
    # O modelo retorna valores normalizados; o resultado deve estar desnormalizado.
    expected = predictor._inverse_transform(
        model_output[:, -PRED_LEN:, :N_TARGETS].astype(np.float64)
    )
    np.testing.assert_allclose(result, expected, rtol=1e-5)


async def test_predict_feeds_model_with_expected_shapes(settings, input_df):
    session = FakeOnnxSession(np.zeros((1, PRED_LEN, N_FEATURES), dtype=np.float32))
    predictor = Predictor(session, settings)

    await predictor.predict(input_df)

    batch_x = session.last_inputs["batch_x"]
    batch_x_mark = session.last_inputs["batch_x_mark"]
    assert batch_x.shape == (1, SEQ_LEN, N_FEATURES)
    assert batch_x.dtype == np.float32
    assert batch_x_mark.shape == (1, SEQ_LEN, 5)
    assert batch_x_mark.dtype == np.float32


def test_inverse_transform_roundtrip(settings):
    predictor = Predictor(FakeOnnxSession(None), settings)
    rng = np.random.default_rng(0)
    original = rng.normal(size=(1, PRED_LEN, N_TARGETS))

    dummy = np.zeros((PRED_LEN, predictor.scaler.n_features_in_))
    dummy[:, :N_TARGETS] = original[0]
    normalized = predictor.scaler.transform(dummy)[:, :N_TARGETS][np.newaxis, ...]

    restored = predictor._inverse_transform(normalized)
    np.testing.assert_allclose(restored, original, rtol=1e-9)


def test_missing_scaler_fails_fast(tmp_path):
    settings = PredictorSettings(
        seq_len=SEQ_LEN,
        pred_len=PRED_LEN,
        n_targets=N_TARGETS,
        scale=True,
        scalers_path=str(tmp_path / "nao_existe"),
    )
    with pytest.raises(FileNotFoundError):
        Predictor(FakeOnnxSession(None), settings)


def test_settings_from_config_requires_mandatory_keys():
    with pytest.raises(ValueError, match="seq_len"):
        PredictorSettings.from_config({"pred_len": 4, "n_targets": 4})


def test_settings_from_config_parses_types():
    settings = PredictorSettings.from_config(
        {"seq_len": "4", "pred_len": 4, "n_targets": 4, "scale": True, "scalers_path": "x/"}
    )
    assert settings.seq_len == 4
    assert settings.scalers_path == "x/"
