

def buy(account, close_price, quantity, time):
    account['USDT'] -= close_price*quantity
    account['quantity'] += quantity
    return {
        'trade' : 'buy',
        'quantity' : quantity,
        'close_price' : close_price,
        'time' : time
    }

def sell(account, close_price, quantity, time):
    account['USDT'] += close_price*quantity
    account['quantity'] -= quantity
    return {
        'trade' : 'sell',
        'quantity' : quantity,
        'close_price' : close_price,
        'time' : time
    }

# basic risk management for now
def risk_management(account, buy_price, current_price, time):
    if((current_price - buy_price)/buy_price >= 0.1):
        return sell(account, current_price, account['quantity'], time)

    if((current_price - buy_price)/buy_price <= -0.1):
        return sell(account, current_price, account['quantity'], time)