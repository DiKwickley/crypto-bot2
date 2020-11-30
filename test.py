#this module is for testing other modules before adding them

import matplotlib.pyplot as plt
import pandas as pd


# modules made by me
from history import get_history
from ichimoku import get_ichimoku



df = get_history('ETHUSDT', 600)

ichimoku = get_ichimoku(df)



# plt.plot(ichimoku.time, ichimoku.tenken_sen, label="tenken_sen (conversion)", color="green", linewidth=.5)
# plt.plot(ichimoku.time, ichimoku.kijun_sen, label="kijun_sen (base)", color="red", linewidth=.5)
plt.fill_between(ichimoku.time, ichimoku.senkou_a, ichimoku.senkou_b, label='senkou clound', color="lightgray")
plt.plot(ichimoku.time, ichimoku.close, label="close", color="blue", linewidth=1)

plt.legend()
plt.show()

# plt.plot( df['time'], df['close'])
# plt.ylabel('price')
# plt.xlabel('time')
# plt.show()
