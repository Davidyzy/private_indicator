theta = np.linalg.inv(x_b.T.dot(x_b)).dot(x_b.T).dot(y)

def polyreg(y):
    x = np.array(list(range(len(y)))
    X = np.column_stack((x**2, x, np.ones_like(x)))

    coefficients = np.linalg.solve(X.T @ X, X.T @ y)
    return coefficients[1]

def alpha1(df, n):
    m = len(df)
    df['VolChange'] = df['LastVol'] - df['LastVol'].shift(1)
    alpha = [0] * len(df)
    alphal = [0] * len(df)

    i = n
    while i < len(df) - 60:
        if df['VolChange'][i] > np.mean(df['VolChange'][i-n:i]) * 3:
            if df['Last'][i] > df['Last'][i-1]:
                alpha[i] = 1
            if df['Last'][i] < df['Last'][i-1]:
                alphal[i] = -1
        i += 1
    df['suddenvolup'] = alpha
    df['suddenvoldown'] = alphal
    return df

def alpha2(df, n):
    df['ma5'] = df['Last'].rolling(5).mean()
    df['ma10'] = df['Last'].rolling(10).mean()
    df['ma20'] = df['Last'].rolling(20).mean()
    df['ma510gap'] = df['ma5'] - df['ma10']
    df['ma1020gap'] = df['ma10'] - df['ma20']
    df['ma520gap'] = df['ma5'] - df['ma20']
    df['Linearregma510gap'] = df['ma510gap'].rolling(n).apply(Linearreg)
    df['Linearregma1020gap'] = df['ma1020gap'].rolling(n).apply(Linearreg)
    df['Linearregma520gap'] = df['ma520gap'].rolling(n).apply(Linearreg)
    
    return df




def cell_kernel_widgets_help(df):
    df['vwap_deviation'] = df['Last'] - df['Last'].shift(1)
    df['vwap_slope'] = df['vwap'].diff()
    df['vwap_momentum'] = df['vwap'].pct_change()
    df['vwap_ratio'] = df['Last'] / df['Last'].shift(1)
    
    n = 30
    df['linearreg_vwap_deviation'] = df['vwap_deviation'].rolling(n).apply(linearreg)
    df['vwap_destd'] = df['vwap_deviation'].rolling(n).std()
    df['vwap_demean'] = df['vwap_deviation'].rolling(n).mean()
    df['vwapstd'] = df['vwap'].rolling(n).std()
    
    return df

def alpha5(df):
    n = 30
    hcvol = [0] * len(df)
    lcvol = [0] * len(df)
    hep = [0] * len(df)
    lep = [0] * len(df)
    
    i = n
    while i < len(df):
        h = [0] * n
        l = [0] * n
        hp = [0] * n
        lp = [0] * n
        for j in range(n):
            if df['Last'][i - n + j] > df['Last'][i]:
                h[j] = df['BidVol'][i - n + j]
                hp[j] = df['Bid'][i - n + j]
            if df['Last'][i - n + j] < df['Last'][i]:
                l[j] = df['AskVol'][i - n + j]
                lp[j] = df['Ask'][i - n + j]
        hcvol[i] = np.sum(h)
        lcvol[i] = np.sum(l)
        hep[i] = np.mean([x for x in hp if x != 0]) / df['Last'][i]
        lep[i] = np.mean([x for x in lp if x != 0]) / df['Last'][i]
        
    df['hcvol'] = hcvol / df['BidVol'].rolling(n).sum()
    df['levol'] = lcvol / df['AskVol'].rolling(n).sum()
    
    return df



import pandas as pd

def calculate_bid_volume_change(df, n):
    df['BidVolChange'] = df['BidVol'] - df['BidVol'].shift(n)
    df['BidVol2Change'] = df['BidVol2'] - df['BidVol2'].shift(n) + df['bidvichange']
    df['BidVol3Change'] = df['BidVol3'] - df['BidVol3'].shift(n) + df['bidv2change']
    df['BidVol4Change'] = df['BidVol4'] - df['BidVol4'].shift(n) + df['bidv3change']
    df['BidVol5Change'] = df['BidVol5'] - df['BidVol5'].shift(n) + df['bidv4change']
    df['AskVolChange'] = df['AskVol'] - df['AskVol'].shift(n)
    df['AskVol2Change'] = df['AskVol2'] - df['AskVol2'].shift(n) + df['askvichange']
    df['AskVol3Change'] = df['AskVol3'] - df['AskVol3'].shift(n) + df['askv2change']
    df['AskVol4Change'] = df['AskVol4'] - df['AskVol4'].shift(n) + df['askv3change']
    df['AskVol5Change'] = df['AskVol5'] - df['AskVol5'].shift(n) + df['askv4change']

    df['VichangeRatio'] = 1 / (df['AskVolChange'] + df['BidVolChange'] + 0.5)
    df['V2ChangeRatio'] = df['bidv2change'] / (df['AskVol2Change'] + df['BidVol2Change'] + 0.5)
    df['V3ChangeRatio'] = df['bidv3change'] / (df['AskVol3Change'] + df['BidVol3Change'] + 0.5)
    df['V4ChangeRatio'] = df['bidv4change'] / (df['AskVol4Change'] + df['BidVol4Change'] + 0.5)
    df['V5ChangeRatio'] = df['bidv5change'] / (df['AskVol5Change'] + df['BidVol5Change'] + 0.5)

    df['VolChange'] = df['LastVol'] - df['LastVol'].shift(1)
    df['BidVolChangePercent'] = df['BidVolChange'] / (df['VolChange'] + 0.5)
    df['BidVol2ChangePercent'] = df['BidVol2Change'] / (df['VolChange'] + 0.5)
    df['BidVol3ChangePercent'] = df['BidVol3Change'] / (df['VolChange'] + 0.5)
    df['BidVol4ChangePercent'] = df['bidvachange'] / (df['VolChange'] + 0.5)
    df['BidVol5ChangePercent'] = df['bidv5change'] / (df['VolChange'] + 0.5)
    df['AskVolChangePercent'] = df['AskVolChange'] / (df['VolChange'] + 0.5)
    df['AskVol2ChangePercent'] = df['AskVol2Change'] / (df['VolChange'] + 0.5)
    df['AskVol3ChangePercent'] = df['AskVol3Change'] / (df['VolChange'] + 0.5)
    df['AskVol4ChangePercent'] = df['askv4change'] / (df['VolChange'] + 0.5)
    df['AskVol5ChangePercent'] = df['AskVol5Change'] / (df['VolChange'] + 0.5)

    tempname = ['Bid', 'Bid2', 'Bid3', 'Bid4', 'Bid5', 'Ask', 'Ask2', 'Ask3', 'Ask4', 'Ask5']

    i = 1
    bidlastpricevolgap = [0] * len(df)
    asklastpricevolgap = [0] * len(df)
    bidrevlastpricevolgap = [0] * len(df)
    askrevlastpricevolgap = [0] * len(df)

    while i < len(df):
        temp = df['Bid'][i]
```