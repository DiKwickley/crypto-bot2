import matplotlib.pyplot as plt
import pandas as panda


# modules made by me
from history import get_history


def get_bollinger(candle_data, sd, n):

    bollinger = panda.DataFrame()
    bollinger['unixtime'] = candle_data['unixtime']
    bollinger['time'] = candle_data['time']
    bollinger['close'] = candle_data['close']
    bollinger['open'] = candle_data['open']
    bollinger['high'] = candle_data['high']
    bollinger['low'] = candle_data['low']


    rolling_mean = candle_data['close'].rolling(window=n, min_periods=n).mean()
    rolling_sd = candle_data['close'].rolling(window=n, min_periods=n).std()
    bollinger['upper_band'] = rolling_mean + (rolling_sd*sd)
    bollinger['lower_band'] = rolling_mean - (rolling_sd*sd)
    bollinger['ma'] = rolling_mean

    return bollinger

# history = get_history('ETHUSDT', 200)

# print('history \n', history)

# bollinger = get_bollinger(history, 1, 20)

# print('donchian \n',bollinger)

# plt.plot(bollinger.time, bollinger.upper_band, label="upper band", color="red", linewidth=2)
# plt.plot(bollinger.time, bollinger.lower_band, label="lower band", color="red", linewidth=2)
# # plt.fill_between(bollinger.time, bollinger.upper_band, bollinger.lower_band, label='senkou clound', color="")
# plt.plot(bollinger.time, bollinger.close, label="close", color="blue", linewidth=1)

# plt.legend()
# plt.show()
