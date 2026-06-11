import pandas as pd
import numpy as np
from src.domain.interfaces.predictor_input_converter import PredictorInputConverter


class PandasPredictorInputConverter(PredictorInputConverter):
    def convert(self, records: list[dict]):
        df = pd.DataFrame(records)
        df["DATE"] = pd.to_datetime(df["DATE"], unit="s", utc=True)
        return df
    def convert_to_matrix(self, data: pd.DataFrame) -> np.ndarray:
        """
        Retorna o array numpy já pronto para o modelo/ml.
        """
        return data.values.astype(np.float32)