__Author__ = 'XMY'

import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff


def signal(*args):
    # 平均每笔成交，看此分钟是否有大单出现

    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df[factor_name] = df['quote_volume'].rolling(n, min_periods=1).sum() / df['trade_num'].rolling(n, min_periods=1).sum()

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df