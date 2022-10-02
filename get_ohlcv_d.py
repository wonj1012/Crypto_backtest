import ccxt
import numpy as np
import pandas as pd
import datetime as dt
from constant import *
from pprint import pprint
import time
import os.path

def str_to_timestamp(datetime_str):
    timestamp_ms = time.mktime(dt.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').timetuple()) * 1000
    
    return int(timestamp_ms)

def get_ohlcv_df(binance, since=None, limit=2000):
    ohlcv = binance.fetch_ohlcv(symbol, timeframe='1d', since=since, limit=limit)
    df = pd.DataFrame(ohlcv, columns = ['time', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = [dt.datetime.fromtimestamp(float(time)/1000) for time in df['time']]
    df.set_index('time', inplace=True)
    
    return df

with open("keys/bnc.key") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret  = lines[1].strip()

binance = ccxt.binance(config={
    'apiKey': api_key, 
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

symbols = symbols[:1]

for symbol in symbols:

    file_path = f"data/day/{symbol[:-5]}.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, index_col="time")

        start_time = str_to_timestamp(df.index[-1])
        df_append = get_ohlcv_df(binance, since=start_time)

        df = pd.concat([df, df_append])
        df.to_csv(file_path)

    else:
        df = get_ohlcv_df(binance)
        df.to_csv(file_path)
