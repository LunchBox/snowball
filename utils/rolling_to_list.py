import numpy as np

def flat(arr, length):
    na = arr.reshape(-1)
    return np.pad(na, (length - len(na), 0))

def rolling_to_list(df, rolling_len):
    """將 rolling 結果轉成行"""
    size = df.shape[1] * rolling_len
    ds = [flat(w.values, size) for w in df.rolling(rolling_len)]
    return ds