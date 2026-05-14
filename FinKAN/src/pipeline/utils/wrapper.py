import torch.nn as nn
import torch


class ProductionWrapper(nn.Module):
    def __init__(self, model, args):
        super().__init__()
        self.model = model
        self.args = args
        self.label_len = args.label_len
        self.pred_len = args.pred_len

    def forward(self, x_enc, x_mark_enc):
        dec_inp_token = x_enc[:, -self.label_len:, :]
        zeros = torch.zeros(
            x_enc.size(0), self.pred_len, x_enc.size(2),
            device= x_enc.device, dtype=x_enc.dtype
        )
        x_dec = torch.cat([dec_inp_token, zeros], dim=1)

        x_mark_dec = torch.zeros(
            x_enc.size(0), self.label_len + self.pred_len, x_mark_enc.size(2),
            device=x_enc.device, dtype=x_enc.dtype
        )

        output = self.model(x_enc, x_mark_enc, x_dec, x_mark_dec)
        output = output[:, -self.pred_len:, :self.args.n_targets]

        return output
