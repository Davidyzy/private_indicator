#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy  as np
import pandas as pd
import talib as ta
from utils.diff import add_diff, eps


def signal(*args):
    # Clv 指标
    df = args[0]
    n = args[1]
    diff_num = args[2]
    factor_name = args[3]

    # CLV=(2*CLOSE-LOW-HIGH)/(HIGH-LOW)
    df['CLV'] = (2 * df['close'] - df['low'] - df['high']) / (df['high'] - df['low'])
    df[factor_name] = df['CLV'].rolling(n, min_periods=1).mean()  # CLVMA=MA(CLV,N)

    # 删除多余列
    del df['CLV']

    if diff_num > 0:
        return add_diff(df, diff_num, factor_name)
    else:
        return df
