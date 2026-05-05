import math
import torch
import torch.nn as nn
from layers.KANLinear import KANLinear

class DataEmbedding_inverted(nn.Module):
    def __init__(self, c_in, d_model, grid_size, dropout=0.1):
        super(DataEmbedding_inverted, self).__init__()
        self.value_embedding = nn.Linear(c_in, d_model)
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, x, x_mark):
        x = x.permute(0, 2, 1)
        if x_mark is not None:
            x_mark = x_mark.permute(0, 2, 1)
            x = torch.cat([x, x_mark], dim=1)
        x = self.value_embedding(x)

        return self.dropout(x)