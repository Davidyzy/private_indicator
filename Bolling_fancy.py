__Author__ = 'XMY'

import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff


def signal(*args):
    # 布林线变种

    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df[factor_name] = (df['close'] - df['close'].rolling(n, min_periods=1).mean()) / df['close'].rolling(n, min_periods=1).std()

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df

