__Author__ = 'XMY'

import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff


def signal(*args):
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]
    df['ma24'] = (talib.EMA(df["close"], timeperiod=24 * n) + df['close'].rolling(2 * 24 * n, min_periods=1).mean()
                + df['close'].rolling(4 * 24 * n, min_periods=1).mean()) / 3
    # 绘制模型走势图
    df[factor_name] = (df['close'] - df['ma24']) / df['ma24']
    # 删除多余列
    del df['ma24']
    # del df['ma4'], df['ma6'], df['ma9'], df['ma13'], df['ma18'], df['ma24']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df