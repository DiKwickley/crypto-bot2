from binance.client import Client
from binance.websockets import BinanceSocketManager
import pprint
import datetime
import pandas
from termcolor import colored
import sys
import os
import pymongo


symbol = sys.argv[1]
time_interval = sys.argv[2]


# config database
mongo_uri = "mongodb+srv://dikwickley:Aniketsprx077@cluster0.jcy0v.mongodb.net/bot2?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_uri)
print(colored("connected to database", 'white', 'on_green'))
db = client["bot2"]
reports = db['reports']
if not reports.find_one({ "$and": [{"pair": symbol}, {"interval": time_interval}]}):
    pair = {
        "pair" : symbol,
        "interval" : time_interval,
        "report" : {}
    }
    reports.insert_one(pair)


#just to print dict objects nicely
pp = pprint.PrettyPrinter(depth=4)

#clear output after each candle, just for better viewings
def clear():
    print('\n\n\n\n\n\n\n\n\n\n\n')


# functions I made
from history import get_history
from ichimoku import get_ichimoku
from donchian import get_donchian
from bollinger import get_bollinger
# from risk import risk_management

now = datetime.datetime.now()
testing_start_at = now.strftime("%d-%m-%Y %H:%M:%S")


all_trade = []
trade = {
    'trade_status' : False,
    'trade_percentage' : 0,
    'current_price' : None,
    'current_open' : None,
    'buy_price' : None,
    'buy_time' : None,
    'sell_price' : None,
    'sell_time' : None
}



#binance API KEYS [place them in enviroment file later]
api_key = 'Ucm9Bk2CxeXjBbkbYO8psVZpbJG6V1VUfco6AD3DVsFpipYyra2fsPrjLnRGLDo2'
api_secret = 'yauS1RGW7x2BaWf83bhPfF8ENQutcZ1W3fDFQEWA9xQm22ZkUNxomtHwyAc8zvQz'

#getting history of last 100 minutes
#minimum would be 53, for ichimoku maximum would be 1000
candle_sticks = get_history(symbol, time_interval, 100)

#frame for indicator
kline  = pandas.DataFrame()


#preparing frame for indicator
kline['unixtime'] = candle_sticks['unixtime']
kline['open'] = candle_sticks['open']
kline['high'] = candle_sticks['high']
kline['low'] = candle_sticks['low']
kline['close'] = candle_sticks['close']
kline['time'] = candle_sticks['time']

#displaying the frame
print("HISTORICAL KLINE: \n",kline)

# listning to  output (res) of socket connection
def socket_output(res):

    clear()

    print('=====================================================================================================================')

    global kline #history
    global all_trade

    # arranging the data from the result of socket connection in a dataframe
    row = pandas.DataFrame([{'time' : res['k']['T'], 'open' : res['k']['o'], 'high': res['k']['h'], 'low': res['k']['l'] ,'close': res['k']['c']}])

    #if candle is closed or not
    if(res['k']['x']):
        # last candle closed start new candle
        kline = kline.iloc[1:]  #pop top candle
        kline = kline.append(row) #push at bottom
    else:
        #update the last candle
        kline.iloc[-1] = [res['k']['T'], res['k']['o'],res['k']['h'], res['k']['l'], res['k']['c'], datetime.datetime.fromtimestamp(res['k']['T']/1000.0)]

    # print(kline)


    ichimoku_frame = get_ichimoku(kline) #the result data containing ichimoku with close and open
    # donchian_frame = get_donchian(kline, 20)
    bollinger2_frame = get_bollinger(kline, 2, 20)
    bollinger1p5_frame = get_bollinger(kline, 1.5, 20)
    

    


    print(colored('Current Time: ' + str(datetime.datetime.fromtimestamp(res['E']/1000.0)), 'blue', 'on_white')) #current time


    ############# STRATEGY HERE ###################################

    global trade

    # previous_candle_open = float(bollinger2_frame.open.iloc[-2])
    # previous_candle_close = float(bollinger2_frame.close.iloc[-2])
    # previous_candle_low = float(bollinger1p5_frame.low.iloc[-2])
    # previous_bollinger_mean = float(bollinger2_frame.ma.iloc[-2])
    # current_candle_close = float(bollinger2_frame.close.iloc[-1])
    # current_bollinger_mean = float(bollinger2_frame.ma.iloc[-1])
    # current_bollinger2_upper = float(bollinger2_frame.upper_band.iloc[-1])
    # current_bollinger1p5_upper = float(bollinger1p5_frame.upper_band.iloc[-1])
    
    current_close = float(ichimoku_frame.close.iloc[-1])
    current_open = float(ichimoku_frame.open.iloc[-1])
    current_time = ichimoku_frame.time.iloc[-1]
    current_bollinger2_upper = float(bollinger2_frame.upper_band.iloc[-1])
    current_bollinger1p5_upper = float(bollinger1p5_frame.upper_band.iloc[-1])
    current_bollinger2_lower = float(bollinger2_frame.lower_band.iloc[-1])
    current_bollinger1p5_lower = float(bollinger1p5_frame.lower_band.iloc[-1])
    current_senkou_a = float(ichimoku_frame.senkou_a.iloc[-1])
    current_senkou_b = float(ichimoku_frame.senkou_b.iloc[-1])



    #trigger values
    price_in_lower_bollinger = current_close > current_bollinger2_lower and current_close < current_bollinger1p5_lower
    price_above_cloud = current_close > current_senkou_a and current_close > current_senkou_b
    price_cross_upper_bollinger = current_close > current_bollinger1p5_upper



    print(colored('Triggers', 'red', 'on_white'))
    print('price_above_cloud ', price_above_cloud)
    print('price_in_lower_bollinger ', price_in_lower_bollinger)
    print('price_cross_upper_bollinger ', price_cross_upper_bollinger)
    

    ##  buying trigger
    if not trade['trade_status'] and price_above_cloud and price_in_lower_bollinger:
        trade['trade_status'] = True
        #buy function here
        trade['buy_price'] = current_close
        trade['buy_time'] = current_time


    ## updating trade object values 
    trade['current_price'] = current_close
    trade['current_open'] = current_open
    #updating trade precentage
    if trade['trade_status'] and trade['buy_price']:
        trade['trade_percentage'] = (current_close - trade['buy_price'])/trade['buy_price']*100

    ## selling trigger
    if trade['trade_status'] and (price_cross_upper_bollinger or trade['trade_percentage'] < -2):
        trade['trade_status'] = False
        # sell function here
        trade['sell_price'] = current_close
        trade['sell_time'] = current_time
        trade['percentage_after_brokerage'] = trade['trade_percentage'] - 0.1

        all_trade.append(trade) # recording the trade
        #resetting trade object
        trade = {
            'trade_status' : False,
            'trade_percentage' : 0,
            'current_price' : None,
            'current_open' : None,
            'buy_price' : None,
            'buy_time' : None,
            'sell_price' : None,
            'sell_time' : None
        }

    print('=====================================================================================================================')

    print(colored('CURRENT TRADE\n', 'magenta'))
    print(colored(pandas.DataFrame([trade]), 'grey', 'on_white'))

    print(colored('ALL TRADES\n', 'magenta'))
    print(pandas.DataFrame(all_trade))

    try:
        print("cummilative %: ", pandas.DataFrame(all_trade).percentage_after_brokerage.sum())
    except:
        print("could not print cummilative %")

    print('=====================================================================================================================')
    ############# STRATEGY END ###################################
    print(colored('Symbol: '+ symbol, 'cyan'))
    print(colored('Interval:  ' + time_interval , 'cyan'))
    print(colored(('Testing started at', testing_start_at),'cyan'))
    # pandas.DataFrame(all_trade).to_csv('./reports/'+ symbol+testing_start_at+'.csv')
    print('=====================================================================================================================')
    query = { "$and" : [{"pair" : symbol} , {"interval" : time_interval}] }
    update = {
        "$set": {
            "report" : {
                "current_time" : str(datetime.datetime.fromtimestamp(res['E']/1000.0)),
                "current_trade" : trade,
                "all_trades" : all_trade,
                "testing_started_at" : testing_start_at
            }
        }
    }
    u = reports.update_one(query, update)
    print('updated: ', u)
# client object of binance
client = Client(api_key, api_secret)
# bm socket manager
bm = BinanceSocketManager(client)
# setting up socket connection for kline
kline_conn = bm.start_kline_socket(symbol, socket_output, interval=time_interval)
# start the connection
bm.start()
