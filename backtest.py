import matplotlib.pyplot as plt
import pandas as pd
import pprint
from tabulate import tabulate 

pp = pprint.PrettyPrinter(depth=4)

from history import get_history
from ichimoku import get_ichimoku
from strategybasic import basic_strategy

#---------------INTERFACE---------------------
symbol = 'ETHUSDT'
limit = 300 #max 1000
indicatorlimit = 100

strategy_obj = {
    'focus_zone': False,     # make true when focus zone starts  
    'focus_start' : None,    # will have start time and price
    'focus_end' : None,      # will have end time and price
    'start_price' : None,    # price at start of focus zone 
    'end_price' : None,      # price at end of focus zone
    'trade' : -1,        # only one trade per focus zone 
                         # -1: no trade | 0: in trade | 1: trade completed for this focus
}
#---------------------------------------------

data = get_history(symbol, limit)

result = []


frame = data[0:indicatorlimit]    #used for making the indicator
backtestdata = data[-1*(data.shape[0]-indicatorlimit):] #rest of the data used for testing further


#for loop for running backtest
for index, row in backtestdata.iterrows():
    print("index:", index)
    frame = frame.iloc[1:]      #for poping first row
    frame = frame.append(row)   #for adding new row
    print('frame')
    print(frame)
    strategy_obj = basic_strategy(frame, strategy_obj)
    print("strategy_obj")
    pp.pprint(strategy_obj)

    #appending the focus zones
    if strategy_obj['focus_end'] and strategy_obj['focus_start']:
        result.append(strategy_obj)
        #resting the strategy object
        strategy_obj = {
            'focus_zone': False,     
            'focus_start' : None,
            'start_price' : None,
            'end_price' : None,
            'focus_end' : None,      
            'trade' : -1,       
                                
        }


    print('---------------------------------------------------------------------------------')

print('result')
print('symbol: ', symbol)
print('data points: ', limit)

result = pd.DataFrame(result)
result = result.drop('focus_zone', axis=1)
print(tabulate(result, headers = 'keys', tablefmt = 'psql')) 