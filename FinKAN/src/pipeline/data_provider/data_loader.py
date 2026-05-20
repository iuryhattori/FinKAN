import os

import warnings

import numpy as np
import pandas as pd
import torch
from sklearn.preprocessing import StandardScaler, RobustScaler
from torch.utils.data import Dataset
import joblib

warnings.filterwarnings('ignore')


class BasePETR4Dataset(Dataset):
    def __init__(self, scale=True, freq='15min', size=None, scalers_path='scalers/'):
        if size == None:
            self.seq_len = 24 * 4 * 4
            self.label_len = 24 * 4
            self.pred_len = 24 * 4
        else:
            self.seq_len = size[0]
            self.label_len = size[1]
            self.pred_len = size[2]
        
        self.scale = scale
        self.freq = freq
        self.scalers_path = scalers_path

    def inverse_transform(self, data):
        if not self.scale:
            return data
        
        is_3d = False
        if len(data.shape) == 3:
            B, T, C = data.shape
            data = data.reshape(-1, C)
            is_3d = True
        else:
            C = data.shape[-1]
        num_features_scaler = self.scaler.n_features_in_

        if C != num_features_scaler:
            dummy = np.zeros((len(data), num_features_scaler))
            dummy[:, :C] = data
            data_denorm = self.scaler.inverse_transform(dummy)[:, :C]
        else:
            data_denorm = self.scaler.inverse_transform(data)

        return data_denorm.reshape(B, T, C) if is_3d else data_denorm
    
class PETR4_dataset(BasePETR4Dataset):
    def __init__(self, root_path, data_path, flag='train', scale=True, freq='15min', size=None, scalers_path='scalers/'):
        super().__init__(scale=scale, freq=freq, size=size, scalers_path=scalers_path)
        assert flag in ['train', 'test', 'val']
        type_map = {'train': 0, 'val': 1, 'test': 2}
        self.set_type = type_map[flag]
        self.scalers_path = scalers_path
        self.root_path = root_path
        self.data_path = data_path
        self.freq = freq
        self.__read_data__()
    def __read_data__(self):
        self.scaler = RobustScaler()
        df_raw = pd.read_csv(os.path.join(self.root_path, self.data_path))

        num_train = int(len(df_raw) * 0.7)
        num_test = int(len(df_raw) * 0.1)
        num_vali = len(df_raw) - num_train - num_test

        border1s = [0, num_train - self.seq_len, int(len(df_raw) - num_test - self.seq_len)]
        border2s = [num_train, num_train + num_vali, len(df_raw)]

        border1 = border1s[self.set_type]
        border2 = border2s[self.set_type]

        cols_base = df_raw.columns[1:]
        self.cols_base = list(cols_base)
        print(f'Colunas Base : {cols_base}')
        df_base = df_raw[cols_base]

        if self.scale:
            train_data = df_base[border1s[0] : border2s[0]]
            self.scaler.fit(train_data.values)
            data = self.scaler.transform(df_base.values)
            if self.set_type == 0:
                scaler_name = os.path.splitext(self.data_path)[0].replace(os.sep, '_')
                scaler_path = os.path.join(self.scalers_path, f'{scaler_name}_scaler.pkl')
                joblib.dump(self.scaler, scaler_path)
                print(f'[Scaler] Treinado e salvo em: {scaler_path}')
                print(pd.DataFrame({
                'Feature' : self.cols_base,
                'Mediana' : self.scaler.center_,
                'IQR'     : self.scaler.scale_
                }).to_string(index=False))
        else:
            data = df_base.values
        data = data.astype(np.float32)

        df_stamp = df_raw[['DATE']][border1 : border2]
        df_stamp['DATE'] = pd.to_datetime(df_stamp.DATE)

        df_stamp['month'] = df_stamp.DATE.apply(lambda row: row.month, 1)
        df_stamp['day'] = df_stamp.DATE.apply(lambda row: row.day, 1)
        df_stamp['weekday'] = df_stamp.DATE.apply(lambda row: row.weekday(), 1)
        df_stamp['hour'] = df_stamp.DATE.apply(lambda row: row.hour, 1)
        df_stamp['minute'] = df_stamp.DATE.apply(lambda row: row.minute, 1)
        df_stamp['minute'] = df_stamp.minute.map(lambda x: x // 15)
        data_stamp = df_stamp.drop(['DATE'], axis= 1).values

        data_stamp = np.asarray(data_stamp, dtype=np.float32)
        self.data_x = data[border1 : border2]    
        self.data_y = data[border1 : border2]
        self.data_stamp = data_stamp
    
    def get_channel_names(self):
        return self.cols_base


    def __getitem__(self, index):
        s_begin = index
        s_end = s_begin + self.seq_len
        r_begin = s_end - self.label_len
        r_end = r_begin + self.label_len + self.pred_len

        seq_x = self.data_x[s_begin : s_end]
        seq_y = self.data_y[r_begin : r_end]
        seq_x_mark = self.data_stamp[s_begin : s_end]
        seq_y_mark = self.data_stamp[r_begin : r_end]
        return seq_x, seq_y, seq_x_mark, seq_y_mark
    def __len__(self):
        return len(self.data_x) - self.seq_len - self.pred_len + 1
    
class PETR4_Prediction(BasePETR4Dataset):
    def __init__(self, df, scale=True, freq='15min', scalers_path = 'scalers/', size=None):
        super().__init__(scale=scale, freq=freq, size=size, scalers_path=scalers_path)
        self.df = df
        self.__read_data__()
    def __read_data__(self):
        df = self.df.copy()
        cols_base = df.columns[1:]
        self.cols_base = list(cols_base)
        print(f'Colunas Base : {cols_base}')
        df_base = df[cols_base]
        if self.scale:
            scaler_fname = 'output_scaler.pkl'
            scaler_path = os.path.join(self.scalers_path, scaler_fname)
            self.scaler = joblib.load(scaler_path)
            data = self.scaler.transform(df_base.values)
        else:
            data = df_base.values
        data = data.astype(np.float32)


        df_stamp = df[['DATE']].copy()
        df_stamp['DATE'] = pd.to_datetime(df_stamp.DATE)


        df_stamp['month'] = df_stamp['DATE'].dt.month
        df_stamp['day'] = df_stamp['DATE'].dt.day
        df_stamp['weekday'] = df_stamp['DATE'].dt.weekday
        df_stamp['hour'] = df_stamp['DATE'].dt.hour
        df_stamp['minute'] = df_stamp['DATE'].dt.minute // 15
        data_stamp = df_stamp.drop(['DATE'], axis=1).values

        data_stamp = np.asarray(data_stamp, dtype=np.float32)
        self.data_x = data
        self.data_stamp = data_stamp

    def __getitem__(self,index):
        s_begin = index
        s_end = s_begin + self.seq_len
        r_begin = s_end - self.label_len
        r_end = r_begin + self.label_len + self.pred_len

        seq_x = self.data_x[s_begin : s_end]
        seq_x_mark = self.data_stamp[s_begin : s_end]
        return seq_x, seq_x_mark
    def __len__(self):
        return len(self.data_x) - self.seq_len + 1