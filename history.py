# probably the heart of the project. get the historical data important for making the indicator

import requests
import pandas as pd
import json
import pprint
import datetime

pp = pprint.PrettyPrinter(depth=4)


def get_history(symbol, time_interval, limit):
    
    # this candle has all the important data for a particular symbol
    candles = requests.get(f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={time_interval}&limit={limit}')
    candles = list(json.loads(candles.text))
    
    history = []

    #arranging the necessary data
    for candle in candles:
        history.append({
            'open' : float(candle[1]),
            'high' : float(candle[2]),
            'low' : float(candle[3]),
            'close' : float(candle[4]),
            'volume' : float(candle[5]),
            'unixtime' : candle[6],
            'time' : datetime.datetime.fromtimestamp(candle[6]/1000.0)

        })
    
    # this line has a lot of significance. this is the start of me using pandas
    # using dataframe will make the program much better
    return pd.DataFrame(history) 



# usage example 
# print(get_history('BTCUSDT', 10))
# yup it's this easy



#candle format {all the data that comes in the candle}
# [
#     1499040000000,      // Open time
#     "0.01634790",       // Open
#     "0.80000000",       // High
#     "0.01575800",       // Low
#     "0.01577100",       // Close
#     "148976.11427815",  // Volume
#     1499644799999,      // Close time
#     "2434.19055334",    // Quote asset volume
#     308,                // Number of trades
#     "1756.87402397",    // Taker buy base asset volume
#     "28.46694368",      // Taker buy quote asset volume
#     "17928899.62484339" // Ignore.
#   ]