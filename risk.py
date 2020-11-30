

def risk_management(trade):
    
    
    current_percentage = (trade['current_price'] - trade['buy_price'])/trade['buy_price']*100

    current_percentage = round(current_percentage,2)

    trade['trade_percentage'] = current_percentage

    # if (round(current_percentage,2)*100)%5 == 0 or (round(current_percentage,2)*100)%5 == 1 or(round(current_percentage,2)*100)%5 == 4:
    #     trade['last_level'] = round(current_percentage,2)

    # print('current:',current_percentage)
    # print('current int round percentage', int(current_percentage*100))
    # if (int(current_percentage*100) > int(trade['last_level']*100)):
    #     trade['last_level'] = current_percentage - (current_percentage%0.20) - 0.1

    # if current_percentage >= 1:
    #     trade['sell_signal'] = True

    # if current_percentage < -0.05:
    #     trade['sell_signal'] = True


    # if trade['last_level'] > 0: #+ve means profit:
    #     if current_percentage < trade['last_level']: 
    #         trade['sell_signal'] = True
    


    

    return trade