__Author__ = 'XMY'

import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff


def signal(*args):
    # 过去一段时间的上行波动率与下行波动率之差

    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['ret_up'] = df['close'].pct_change()
    df['ret_down'] = df['ret_up']
    df.loc[df['ret_up'] > 0, 'ret_down'] = np.nan
    df.loc[df['ret_up'] < 0, 'ret_up'] = np.nan

    df[factor_name] = df['ret_up'].rolling(n, min_periods=1).std() - df['ret_down'].rolling(n, min_periods=1).std()

    del df['ret_up'], df['ret_down']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df