from ichimoku import get_ichimoku

'''
checks to be done:
    ALL This is just to enter a trade. Risk Managenment has to be adjusted accoring to 1 min chart
    
    - two closes above ichimoku cloud
    - the percentage of second candle (close - open)/open*100 should be less than some CERTAIN percentage
        if so, do not take trade in that focus zones
    - the percentage of second candle (close - open)/open*100 should be greater than the first candle
        if so, do not take trade in that focus zones
    - low of second candle should be above the cloud
    - increase the senkou_a and senkou_b by some percentage to get rid of weird data


'''
    

def basic_strategy(frame, strategy_obj):
    
    ichimoku = get_ichimoku(frame)

    #slicing the ichimoku to check for a range of values
    ichimoku = ichimoku[-1]

    


    # print(ichimoku)
    return strategy_obj