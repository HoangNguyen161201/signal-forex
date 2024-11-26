from pygame import mixer  # Load the popular external library
from oder import place_stop, get_price_older, get_current_price, CalculateLotSize, close_position, place_order
import MetaTrader5 as mt5
import threading
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from datetime import datetime
import pytz

print("start")

#info
symbol = input('nhập tên symbol (BTCUSD):')
distance_lot_check = int(input('nhập khoản cách giá để tạo lot (100):'))
price_check = 0

def play_sound():  
    mixer.init()
    mixer.music.load('./ring.mp3')
    mixer.music.play()

def edit_file(text):
    with open('output.txt', 'a', encoding='utf-8') as file:
        vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
        now_vietnam = datetime.now(vietnam_tz)
        formatted_time = now_vietnam.strftime('%H:%M %d-%m-%Y')
        file.write(f"{formatted_time} {text}\n")

while True:
    try:
        tv = TvDatafeed()
        nifty_index_data = tv.get_hist(symbol= symbol,exchange='CAPITALCOM',interval=Interval.in_5_minute,n_bars=3)
        
        candle_1_state = {
            'open': nifty_index_data.iloc[0]['open'],
            'close': nifty_index_data.iloc[0]['close'],
            'high': nifty_index_data.iloc[0]['high'],
            'low': nifty_index_data.iloc[0]['low'] 
        }
        candle_2_state = {
            'open': nifty_index_data.iloc[1]['open'],
            'close': nifty_index_data.iloc[1]['close'],
            'high': nifty_index_data.iloc[1]['high'],
            'low': nifty_index_data.iloc[1]['low']  
        }

        print(candle_1_state['low'])

    
        is_buy_1 = False if candle_1_state['open'] > candle_1_state['close'] else True
        is_buy_2 = False if candle_2_state['open'] > candle_2_state['close'] else True


        if(price_check != candle_1_state['close']):
            if(is_buy_1 and not is_buy_2):
                body_1 = candle_1_state['close'] - candle_1_state['open']
                body_2 = candle_2_state['open'] - candle_2_state['close']
                if(body_2 <= body_1 / 2 and candle_2_state['low'] > candle_1_state['open']):
                    lot = CalculateLotSize(candle_1_state['high'] if candle_1_state['high'] > candle_2_state['high'] else candle_2_state['high'], candle_2_state['low'], distance_lot_check)
                    text = f"{symbol}-buy-{lot}"
                    edit_file(text)
                    threading.Thread(target=play_sound).start()
            if(not is_buy_1 and is_buy_2):
                body_1 = candle_1_state['open'] - candle_1_state['close']
                body_2 = candle_2_state['close'] - candle_2_state['open']
                if(body_2 <= body_1 / 2 and candle_2_state['high'] < candle_1_state['open']):
                    lot = CalculateLotSize(candle_1_state['low'] if candle_1_state['low'] < candle_2_state['low'] else candle_2_state['low'], candle_2_state['high'], distance_lot_check)
                    text = f"{symbol}-sell-{lot}"
                    edit_file(text)
                    threading.Thread(target=play_sound).start()
        price_check = candle_1_state['close']
    except:
        print('An exception occurred')


