import pandas as pd
from src.domain.interfaces.predictor_input_converter import PredictorInputConverter


class PandasPredictorInputConverter(PredictorInputConverter):
    def convert(self, records: list[dict]):
        df = pd.DataFrame(records)
        df["DATE"] = pd.to_datetime(df["DATE"], unit="s", utc=True)
        return df