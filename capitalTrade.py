from pygame import mixer  # Load the popular external library
from oder import place_stop, get_price_older, CalculateLotSize, close_order_by_magic_number
import MetaTrader5 as mt5
import threading
from capital_func import CapitalcomData
import capitalcom

print("start")
capitalcom_data = CapitalcomData('BTCUSD')

#info
symbol_tradingview = 'BTCUSD'
price_check = 0

def play_sound():  
    mixer.init()
    mixer.music.load('./ring.mp3')
    mixer.music.play()

def calculate_volume(price1, price2):
    price_difference = abs(price2 - price1)
    volume = round(0.01 / (97.65 / price_difference), 2); 
    return volume

while True:
    try:
        prices = capitalcom_data.get_prices_history(capitalcom.client.ResolutionType.MINUTE_5, 3)
        open1 = prices['prices'][0]['openPrice']['bid'] 
        close1 = prices['prices'][0]['closePrice']['bid'] 
        high1 = prices['prices'][0]['highPrice']['bid'] 
        low1 = prices['prices'][0]['lowPrice']['bid'] 

        open2 = prices['prices'][1]['openPrice']['bid'] 
        close2 = prices['prices'][1]['closePrice']['bid'] 
        high2 = prices['prices'][1]['highPrice']['bid'] 
        low2 = prices['prices'][1]['lowPrice']['bid'] 

        print(f'{open1}-{open2}')
       

        if(price_check != close1):
            is_buy_1 = False if open1 > close1 else True
            is_buy_2 = False if open2 > close2 else True
            if(is_buy_1 and not is_buy_2):
                body_1 = close1 - open1
                body_2 = open2 - close2
                if(body_2 <= body_1 / 2 and low2 > open1):
                    lot = calculate_volume(high1 if high1 > high2 else high2, low2)
                    print(lot)
                    threading.Thread(target=play_sound).start()
            if(not is_buy_1 and is_buy_2):
                body_1 = open1 - close1
                body_2 = close2 - open2
                if(body_2 <= body_1 / 2 and high2 < open1):
                    lot = calculate_volume(low1 if low1 < low2 else low2, high2)
                    print(lot)
                    threading.Thread(target=play_sound).start()
                    
        price_check = close1
    except:
      print('An exception occurred')


