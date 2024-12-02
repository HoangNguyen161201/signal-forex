from pygame import mixer  # Load the popular external library
from oder import place_stop, get_price_older, get_current_price, close_position, place_order, symbols, calculate_lots
import MetaTrader5 as mt5
import threading
import pandas as pd
from tvDatafeed import TvDatafeed, Interval
from datetime import date, datetime
import pytz
import csv


#info
index = int(input('nhập tên index symbol (0 - 3):')) 
price_check = 0
current_price_path = rf'C:\Users\hoang\AppData\Roaming\MetaQuotes\Terminal\B3FBDE368DD9733D40FCC49B61D1B808\MQL4\Files\{symbols[index]['current_price_file']}'
two_candle_price_path = rf'C:\Users\hoang\AppData\Roaming\MetaQuotes\Terminal\B3FBDE368DD9733D40FCC49B61D1B808\MQL4\Files\{symbols[index]['two_candle_price_old_file']}'
candle1 = None
candle2 = None
lot = 0
current_price = 0
is_buy = False
is_hedging = False

print("start")

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


def reset():
    global current_price, index, price_check, current_price_path, two_candle_price_path, candle1, candle2, lot, is_hedging, is_buy
    is_hedging = False
    lot = 0
    candle1 = None
    candle2 = None
    current_price = 0
    price_check = 0
    is_buy = False


def check():
    global index, current_price, price_check, current_price_path, two_candle_price_path, candle1, candle2, lot, is_hedging, is_buy

    tv = TvDatafeed()
    nifty_index_data = tv.get_hist(symbol= symbols[index]['symbol_capital'],exchange='CAPITALCOM',interval=Interval.in_5_minute,n_bars=3)
    
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

    

    is_buy_1 = False if candle_1_state['open'] > candle_1_state['close'] else True
    is_buy_2 = False if candle_2_state['open'] > candle_2_state['close'] else True


    if(price_check != candle_1_state['close']):
        if(is_buy_1 and not is_buy_2):
            body_1 = candle_1_state['close'] - candle_1_state['open']
            body_2 = candle_2_state['open'] - candle_2_state['close']
            if(body_2 <= body_1 / 2 and candle_2_state['low'] > candle_1_state['open']):
                lot = calculate_lots(
                    1,
                    abs((candle_1_state['high'] if candle_1_state['high'] > candle_2_state['high'] else candle_2_state['high']) - candle_2_state['low']),
                    symbols[index]['symbol_robo']
                    )
                text = f"{symbols[index]['symbol_robo']}-buy-{lot}"
                with open(two_candle_price_path, mode="r") as file:
                    reader = csv.reader(file)
                    first_row = next(reader)  # Đọc hàng đầu tiên
                    first_value = first_row[0]
                    if(first_value):
                        data = first_value.split(';')
                        candle1 = {
                            'high': float(data[0]),
                            'low': float(data[1])
                        }
                        candle2 = {
                            'high': float(data[2]),
                            'low': float(data[3])
                        }
                is_buy = True
                edit_file(text)
                threading.Thread(target=play_sound).start()
        if(not is_buy_1 and is_buy_2):
           
            body_1 = candle_1_state['open'] - candle_1_state['close']
            body_2 = candle_2_state['close'] - candle_2_state['open']
            if(body_2 <= body_1 / 2 and candle_2_state['high'] < candle_1_state['open']):
                lot = calculate_lots(
                    1,
                    abs((candle_1_state['low'] if candle_1_state['low'] < candle_2_state['low'] else candle_2_state['low']) - candle_2_state['high']),
                    symbols[index]['symbol_robo']
                    )
                text = f"{symbols[index]['symbol_robo']}-sell-{lot}"
                with open(two_candle_price_path, mode="r") as file:
                    reader = csv.reader(file)
                    first_row = next(reader)  # Đọc hàng đầu tiên
                    first_value = first_row[0]
                    if(first_value):
                        data = first_value.split(';')
                        candle1 = {
                            'high': float(data[0]),
                            'low': float(data[1])
                        }
                        candle2 = {
                            'high': float(data[2]),
                            'low': float(data[3])
                        }
                is_buy = False
                edit_file(text)
                threading.Thread(target=play_sound).start()
    price_check = candle_1_state['close']

def trade():
    global index, current_price, price_check, current_price_path, two_candle_price_path, candle1, candle2, lot, is_hedging, is_buy

    best_high = candle1['high'] if candle1['high'] > candle2['high'] else candle2['high'] 
    best_low = candle1['low'] if candle1['low'] < candle2['low'] else candle2['low'] 
    

    with open(current_price_path, mode="r") as file:
        reader = csv.reader(file)
        first_row = next(reader)  # Đọc hàng đầu tiên
        first_value = first_row[0]
        if(first_value):
            current_price = float(first_value)

    if((is_buy and not is_hedging and current_price < best_low) or 
       (not is_buy and not is_hedging and current_price > best_high)
       ):
        print('không trade được vì không đúng điều kiện')
        reset()
    else:
        if(is_buy and is_hedging and current_price <= ((candle2['high'] + candle2['low']) / 2)):
            print(f'đánh ngược để cân bằng {lot}')
            place_order(symbols[index]['symbol_robo'], mt5.ORDER_TYPE_SELL, lot, 0.0, 0.0, 0.0 )
            reset()
            
        if(not is_buy and is_hedging and current_price >= ((candle2['high'] + candle2['low']) / 2)):
            print(f'đánh ngược để cân bằng {lot}')
            place_order(symbols[index]['symbol_robo'], mt5.ORDER_TYPE_BUY, lot, 0.0, 0.0, 0.0 )
            reset()

        if(is_buy and current_price and current_price > best_high and not is_hedging):
            print(2)
            print(f'buy nha {lot}')
            place_order(symbols[index]['symbol_robo'], mt5.ORDER_TYPE_BUY, lot, 0.0, 0.0, 0.0 )
            is_hedging = True
            lot += lot
        if(not is_buy and current_price and current_price < best_low and not is_hedging):
            print(f'sell nha {lot}')
            place_order(symbols[index]['symbol_robo'], mt5.ORDER_TYPE_SELL, lot, 0.0, 0.0, 0.0 )
            is_hedging = True
            lot += lot

while True:
    try:
        if(candle1 and candle2 and lot):
           trade()
        else:
            check()
    except:
        print('An exception occurred')


