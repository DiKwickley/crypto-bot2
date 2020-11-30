import matplotlib.pyplot as plt
import pandas as panda


# modules made by me
from history import get_history


def get_donchian(candle_data, n):

    donchian = panda.DataFrame()
    donchian['unixtime'] = candle_data['unixtime']
    donchian['time'] = candle_data['time']
    donchian['close'] = candle_data['close']
    donchian['upper'] = candle_data['high'].rolling(window=n, min_periods=n).max()
    donchian['lower'] = candle_data['low'].rolling(window=n, min_periods=n).min()
    donchian['middle'] = (donchian['upper'] + donchian['lower'])/2
    return donchian

# history = get_history('ETHUSDT', 200)

# print('history \n', history)

# donchian = get_donchian(history, 20)

# print('donchian \n',donchian)

# plt.plot(donchian.time, donchian.upper, label="upper line", color="green", linewidth=2)
# plt.plot(donchian.time, donchian.lower, label="lower line", color="green", linewidth=2)
# plt.plot(donchian.time, donchian.middle, label="middle", color="orange", linewidth=.5)
# plt.plot(donchian.time, donchian.close, label="close", color="blue", linewidth=1)

# plt.legend()
# plt.show()