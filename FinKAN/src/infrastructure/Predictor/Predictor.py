from src.pipeline.data_provider.data_factory import data_provider
import pandas as pd
import numpy as np


class Predictor:
    def __init__(self, onnx_model, args):
        self.onnx_model = onnx_model
        self.args = args
        
    async def predict(self, input : pd.DataFrame):
        print("Starting Predictions")
        dataset, data_loader = data_provider(args=self.args, flag='pred', prediction_df=input)
        batch_x, batch_x_mark = next(iter(data_loader))

        x_np = batch_x.numpy().astype(np.float32)
        mk_np = batch_x_mark.numpy().astype(np.float32)

        outputs = self.onnx_model.run(None, {'batch_x': x_np, 'batch_x_mark': mk_np})[0]
        pred = outputs[:, -self.args.pred_len:, :self.args.n_targets]
        pred_desnorm = dataset.inverse_transform(pred)
        return pred_desnorm