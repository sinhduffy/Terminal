import time
import datetime
from worder import data


def check_buy_beak(price_buy):
    price_sell = round(price_buy +20, 2)
    return price_sell


def check_buy_low(price_buy):
    price_sell = round(price_buy * 1.01, 2)
    return price_sell


def check_rate_cot(price_buy):
    price_sell = round(price_buy * 1.005)
    return price_sell


def is_erea(price_buy) :
    price_sell = round(price_buy  * 1.0025)
    return price_sell

def check_Close(price_buy) :
    price_sell = round(price_buy * 1.01)
    return price_sell

def check_RSI(price_buy) :
    price_sell = round(price_buy * 1.02)
    return price_sell


def AI_SELL():
    while True:
        d = datetime.datetime.now()
        timestr = d.strftime('%H:%M:%S')
        df = data.data(symbol, '15m', '30', client)
        price_current = df.Close.iloc[-1]
        check_stoploss_min = price_stoploss + 30
        time.sleep(0.5)
        print(price_current, price_stoploss_min, check_target, check_stoploss_min, end='\r')

        # print('Price_Current :',price_current ,'Price_Stoploss :',round(price_stoploss*0.998,n),end ='\r')
        if price_current <= check_target and price_current <= price_stoploss_min:
            ifsell = True
            sell = True
            print()
            print('Target : ', price_current, 'Time :', timestr)
            break
        elif price_current > check_stoploss_min:
            price_stoploss = price_current
            print()
            print('Change Stoploss : ', price_stoploss, 'Price_stoploss :', round(check_target, 2),
                  'Time :', timestr)
            break
    return price_current