from zmq import Flag

from data_provider.data_loader import PETR4_dataset, PETR4_Prediction
from torch.utils.data import DataLoader

data_dict = {
    'PETR4':  PETR4_dataset,
    'PETR4_Prediction': PETR4_Prediction
}

def data_provider(args, flag, prediction_df = None):
    if flag == 'pred':
        shuffle_flag = False
        drop_last = False
        batch_size = 1
        freq = args.freq
        data_set = PETR4_Prediction(
            df = prediction_df,
            scale = args.scale,
            freq = args.freq,
            scalers_path= args.scalers_path,
            size = [args.seq_len, args.label_len, args.pred_len, args.enc_in]
        )
    elif flag == 'test':
        shuffle_flag = False
        drop_last = False
        batch_size = args.batch_size
        freq = args.freq
        data_set = PETR4_dataset(
            root_path=args.root_path,
            data_path=args.data_path,
            flag=flag,
            size=[args.seq_len, args.label_len, args.pred_len, args.enc_in],
            freq=freq,
            scale=args.scale,
            scalers_path= args.scalers_path,
        )
    else:
        shuffle_flag = True
        drop_last = False
        batch_size = args.batch_size
        freq = args.freq
        data_set = PETR4_dataset(
            root_path=args.root_path,
            data_path=args.data_path,
            flag=flag,
            size=[args.seq_len, args.label_len, args.pred_len, args.enc_in],
            freq=freq,
            scale=args.scale,
            scalers_path= args.scalers_path,
        )
    print(flag, len(data_set))
    data_loader = DataLoader(
        data_set,
        batch_size = batch_size,
        shuffle = shuffle_flag,
        num_workers=args.num_workers,
        drop_last = drop_last,
    )
    return data_set, data_loader
        