import asyncio
import logging
import os

import joblib
import numpy as np
import pandas as pd

from src.infrastructure.config.predictor_settings import PredictorSettings
from src.pipeline.data_provider.data_loader import build_time_features

logger = logging.getLogger(__name__)


class Predictor:
    """Inferência ONNX. O scaler é carregado uma única vez na inicialização."""

    SCALER_FILENAME = "output_scaler.pkl"

    def __init__(self, onnx_model, settings: PredictorSettings):
        self.onnx_model = onnx_model
        self.settings = settings
        self.scaler = self._load_scaler() if settings.scale else None

    def _load_scaler(self):
        scaler_path = os.path.join(self.settings.scalers_path, self.SCALER_FILENAME)
        if not os.path.exists(scaler_path):
            raise FileNotFoundError(f"Scaler não encontrado: {scaler_path}")
        scaler = joblib.load(scaler_path)
        logger.info(f"Scaler carregado de {scaler_path}")
        return scaler

    def _build_inputs(self, input_df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
        """Normaliza as features e monta os tensores (1, seq_len, n_features)."""
        df_base = input_df[input_df.columns[1:]]
        if self.scaler is not None:
            data = self.scaler.transform(df_base.values)
        else:
            data = df_base.values
        data = data.astype(np.float32)

        data_stamp = build_time_features(input_df["DATE"])

        seq_len = self.settings.seq_len
        batch_x = data[:seq_len][np.newaxis, ...]
        batch_x_mark = data_stamp[:seq_len][np.newaxis, ...]
        return batch_x, batch_x_mark

    def _inverse_transform(self, data: np.ndarray) -> np.ndarray:
        if self.scaler is None:
            return data

        B, T, C = data.shape
        flat = data.reshape(-1, C)
        num_features_scaler = self.scaler.n_features_in_

        if C != num_features_scaler:
            dummy = np.zeros((len(flat), num_features_scaler))
            dummy[:, :C] = flat
            flat = self.scaler.inverse_transform(dummy)[:, :C]
        else:
            flat = self.scaler.inverse_transform(flat)
        return flat.reshape(B, T, C)

    async def predict(self, input: pd.DataFrame) -> np.ndarray:
        logger.info("Iniciando predição")
        batch_x, batch_x_mark = self._build_inputs(input)

        # ONNX Runtime é CPU-bound: roda fora do event loop para não travar a API.
        outputs = await asyncio.to_thread(
            self.onnx_model.run,
            None,
            {"batch_x": batch_x, "batch_x_mark": batch_x_mark},
        )
        pred = outputs[0][:, -self.settings.pred_len:, :self.settings.n_targets]
        return self._inverse_transform(pred)
