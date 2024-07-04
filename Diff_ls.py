__Author__ = 'XMY'

import pandas as pd
import numpy as np
import talib
from utils.diff import add_diff


def signal(*args):
    #该指标使用时注意n不能大于过滤K线数量的一半（不是获取K线数据的一半）
    """
    N=20
    M=10
    MA_CLOSE=MA(CLOSE,N)
    MADisplaced=REF(MA_CLOSE,M)
    MADisplaced 指标把简单移动平均线向前移动了 M 个交易日，用法
    与一般的移动平均线一样。如果收盘价上穿/下穿 MADisplaced 则产
    生买入/卖出信号。
    有点变种bias
    """
    df = args[0]
    n  = args[1]
    diff_num = args[2]
    factor_name = args[3]

    df['DIF'] = (talib.EMA(df["close"],timeperiod=12 * n) - talib.EMA(df["close"],timeperiod=26 * n))/talib.EMA(df["close"],timeperiod=26 * n)
    con = (df['DIF']) > 0
    df.loc[con,'RISE'] = 1
    con = (df['DIF']) <= 0
    df.loc[con,'RISE'] = -1

    con1 = (df["DIF"] - df["DIF"].shift(2)) < 0
    df.loc[con1, 'RISE_2'] = -1
    con2 = (df["DIF"] - df["DIF"].shift(2)) >= 0
    df.loc[con2, 'RISE_2'] = 1
    df[factor_name] = df['RISE'] + df['RISE_2']
    df[factor_name].fillna(value=0, inplace=True)
    # 删除多余列
    del df['DIF'], df['RISE'], df['RISE_2']
    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df