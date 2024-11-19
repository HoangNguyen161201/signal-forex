from pygame import mixer  # Load the popular external library
from oder import place_stop, get_price_older, get_current_price, CalculateLotSize, close_position, place_order
import MetaTrader5 as mt5
import threading
import pandas as pd
from tvDatafeed import TvDatafeed, Interval

print("start")

#info
symbol = 'BTCUSD'
price_check = 0
candle_1 = {}
candle_2 = {}
is_start_trade = 0
file_path = rf"C:\Users\hoang\AppData\Roaming\MetaQuotes\Terminal\B3FBDE368DD9733D40FCC49B61D1B808\MQL4\Files\{symbol}.csv"
thap_phan = 2
magic = 1
lot = 0.01

def play_sound():  
    mixer.init()
    mixer.music.load('./ring.mp3')
    mixer.music.play()

while True:
    try:
        if(is_start_trade != 0):
            is_buy_1 = False if candle_1['open'] > candle_1['close'] else True
            best_high = candle_1['high'] if candle_1['high'] > candle_2['high'] else candle_2['high']
            best_low = candle_1['low'] if candle_1['low'] < candle_2['low'] else candle_2['low']
            if(is_start_trade == 1):
                lot = CalculateLotSize(candle_1['high'] if candle_1['high'] > candle_2['high'] else candle_2['high'], candle_2['low']) if is_buy_1 else CalculateLotSize(candle_1['low'] if candle_1['low'] < candle_2['low'] else candle_2['low'], candle_2['high'])
            df = pd.read_csv(file_path, header=None)
            current_price = df.head()[0][0]
            print(current_price)
            if((is_buy_1 and current_price < candle_1['low']) or (not is_buy_1 and current_price > candle_1['high'])):
                is_start_trade = 0

            if(is_buy_1 and current_price > best_high and is_start_trade == 1):
                is_start_trade = 2
                distance = round(best_high - candle_2['low'], 2)
                current_price_exness = get_current_price(symbol)
                tp = round(current_price_exness['bid'] + distance, 2)
                place_order(symbol, mt5.ORDER_TYPE_BUY, lot, 0.0, 0.0, tp, magic)
                magic += 1
                print(f'buy - {lot}')
                threading.Thread(target=play_sound).start()
            if( not is_buy_1 and current_price < best_low and is_start_trade == 1):
                is_start_trade = 2
                distance = round(candle_2['high'] - best_low, thap_phan)
                tp = round(current_price_exness['bid'] - distance, 2)
                place_order(symbol, mt5.ORDER_TYPE_SELL, lot, 0.0, 0.0, tp, magic)
                magic += 1
                print(f'sell - {lot}')
                threading.Thread(target=play_sound).start()

            if((is_start_trade == 2 and is_buy_1 and current_price > (best_high + (best_high - candle_2['low'])))
               or (is_start_trade == 2 and not is_buy_1 and current_price < (best_low - (candle_2['high'] - best_low)))
               or (is_start_trade == 2 and is_buy_1 and current_price <  candle_2['low'])
               or (is_start_trade == 2 and not is_buy_1 and current_price > candle_2['high'])
               ):
                close_position(magic - 1)
                is_start_trade = 0
                candle_1 = {}
                candle_2 = {}
                lot = 0.01 
            
            # if(is_start_trade == 2):
            #     if(is_buy_1 and current_price <= (best_high + (best_high - candle_2['low'])) / 2):
            #         is_start_trade = 0
            #         candle_1 = {}
            #         candle_2 = {}
            #         lot = 0.01 
            #     if(not is_buy_1 and current_price >=  (best_low + (best_low - (candle_2['high'] - best_low)) ) / 2):
            #         is_start_trade = 0
            #         candle_1 = {}
            #         candle_2 = {}
            #         lot = 0.01 
           
        else:
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

        
            is_buy_1 = False if candle_1_state['open'] > candle_1_state['close'] else True
            is_buy_2 = False if candle_2_state['open'] > candle_2_state['close'] else True

            print(f'{candle_1_state['open']}-{candle_1_state['close']}:{candle_2_state['open']}-{candle_2_state['close']}:{is_buy_1}-{is_buy_2}')

            if(price_check != candle_1_state['close']):
                if(is_buy_1 and not is_buy_2):
                    body_1 = candle_1_state['close'] - candle_1_state['open']
                    body_2 = candle_2_state['open'] - candle_2_state['close']
                    if(body_2 <= body_1 / 2 and candle_2_state['low'] > candle_1_state['open']):
                        is_start_trade = 1
                        candle_1 = candle_1_state
                        candle_2 = candle_1_state
                        threading.Thread(target=play_sound).start()
                if(not is_buy_1 and is_buy_2):
                    body_1 = candle_1_state['open'] - candle_1_state['close']
                    body_2 = candle_2_state['close'] - candle_2_state['open']
                    if(body_2 <= body_1 / 2 and candle_2_state['high'] < candle_1_state['open']):
                        is_start_trade = 1
                        candle_2 = candle_2_state
                        candle_1 = candle_1_state
                        threading.Thread(target=play_sound).start()
            price_check = candle_1_state['close']
    except:
        print('An exception occurred')


