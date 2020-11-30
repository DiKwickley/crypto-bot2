import matplotlib.pyplot as plt
import pandas as pd


# modules made by me
from history import get_history


def get_ichimoku(candle_data):    

    ichimoku = pd.DataFrame()

    #adding some data to maintain the integrity later when sockets will be used
    ichimoku['open'] = candle_data['open']
    ichimoku['close'] = candle_data['close']

    
    #Tenkan Sen (conversion line GREEN)
    tenkan_max = candle_data['high'].rolling(window = 9, min_periods = 0).max()
    tenkan_min = candle_data['low'].rolling(window = 9, min_periods = 0).min()
    ichimoku['tenken_sen'] = (tenkan_max + tenkan_min) / 2

    #Kijun Sen (base line RED)
    kijun_max = candle_data['high'].rolling(window = 26, min_periods = 0).max()
    kijun_min = candle_data['low'].rolling(window = 26, min_periods = 0).min()
    ichimoku['kijun_sen'] = (kijun_max + kijun_min) / 2

    #Senkou Span A
    #(Kijun + Tenkan) / 2 Shifted ahead by 26 periods
    ichimoku['senkou_a'] = (round((ichimoku['kijun_sen'] + ichimoku['tenken_sen']) / 2, 2)).shift(26)

    #Senkou Span B
    #52 period High + Low / 2
    senkou_b_max = candle_data['high'].rolling(window = 52, min_periods = 0).max()
    senkou_b_min = candle_data['low'].rolling(window = 52, min_periods = 0).min()
    ichimoku['senkou_b'] = (round((senkou_b_max + senkou_b_min) / 2,2)).shift(26)

    #adding time for sync
    ichimoku['unixtime'] = candle_data['unixtime']
    ichimoku['time'] = candle_data['time']

    return ichimoku


'''
USAGE EXAMPLE
ICHIMOKU takes in historical data dataframe
the dataframe shoudl contain
    -close
    -high
    -low
    -unixtime
    -time

and returns an ichimoku dataframe containing
    -close
    -unixtime
    -time
    -tenken_sen
    -kijun_sen
    -senkou_a
    -senkou_b

'''

# history = get_history('ETHUSDT', 200)

# ichimoku = get_ichimoku(history)

#demo of plotting the indicator

# plt.plot(ichimoku.time, ichimoku.tenken_sen, label="tenken_sen (conversion)", color="green", linewidth=.5)
# plt.plot(ichimoku.time, ichimoku.kijun_sen, label="kijun_sen (base)", color="red", linewidth=.5)
# plt.fill_between(ichimoku.time, ichimoku.senkou_a, ichimoku.senkou_b, label='senkou clound', color="lightgray")
# plt.plot(ichimoku.time, ichimoku.close, label="close", color="blue", linewidth=1)

# plt.legend()
# plt.show()