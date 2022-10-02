import time
import datetime as dt
import pandas as pd
import numpy as np
from constants.constant import *

symbol = "BTC/USDT"
df = pd.read_csv(f"data/day/{symbol[:-5]}.csv", index_col="time")
df.index = pd.to_datetime(df.index)

df['range'] = df['high'] - df['low']
df['long_target'] = df['open'] + df['range'].shift(1) * long_k
df['short_target'] = df['open'] - df['range'].shift(1) * short_k
for i in [2, 3, 5, 7, 10, 14, 21, 30]:
    df[str(i) + 'MA'] = df['close'].rolling(window=i).mean()

df['MT_score'] = 0
for i in [2, 3, 5, 7, 10, 14, 21, 30]:
    df['MT_score'] += np.where(df['open'] > df[str(i) + 'MA'].shift(1), 1, 0)

df = df[27:]
# df['long_buy'] = df['high'] > df['long_target']
# df['short_buy'] = df['low'] < df['short_target']
df['long_drr'] = np.where(df['high'] > df['long_target'], df['close'] / df['long_target'], 1)
df['short_drr'] = np.where(df['low'] < df['short_target'], df['short_target'] / df['close'], 1)
df['drr'] = np.where((df['high'] > df['long_target']) & (df['low'] < df['short_target']), df['short_target'] / df['long_target'], df['long_drr'] * df['short_drr'])
# df['long_crr'] = df['long_drr'].cumprod()
# df['short_crr'] = df['short_drr'].cumprod()

df['asset'] = df['drr'].cumprod()
df['max_asset'] = df['asset'].cummax()

df['dd'] = (df['asset'] / df['max_asset'] - 1)
df['mdd'] = df['dd'].cummin()

print(df)

cagr = df['asset'][-1] ** (365 / len(df)) - 1
print(f"CAGR: {round(cagr * 100, 4)}%\n"
      f"MDD: {round(df['mdd'][-1] * 100, 4)}%\n"
      f"MAR: {round(cagr / df['mdd'][-1] * -1, 4)}")