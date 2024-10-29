from tvDatafeed import TvDatafeed, Interval
from pygame import mixer  # Load the popular external library
from oder import place_stop, get_price_older, CalculateLotSize, close_order_by_magic_number
import MetaTrader5 as mt5
import threading

print("start")

#info
symbol_exness = 'XAUUSD'
symbol_tradingview = 'GOLD'
price_check = 0
is_buy = False
margic_number = 1
is_delete_old_order = True

def play_sound():  
    mixer.init()
    mixer.music.load('./ring.mp3')
    mixer.music.play()

while True:
    try:
        tv = TvDatafeed()
        nifty_index_data = tv.get_hist(symbol= symbol_tradingview,exchange='CAPITALCOM',interval=Interval.in_5_minute,n_bars=2)
        print(f'{nifty_index_data.iloc[0]['close']}-{nifty_index_data.iloc[1]['open']}')
        if(is_delete_old_order == False and price_check != nifty_index_data.iloc[0]['close']):
            new_is_buy = False if nifty_index_data.iloc[0]['open'] < nifty_index_data.iloc[0]['close'] else True
            if(new_is_buy == is_buy):
                close_order_by_magic_number(margic_number - 1)
                is_delete_old_order = True
                print("đã đóng lệnh")

        if(price_check != nifty_index_data.iloc[0]['close'] and nifty_index_data.iloc[0]['close'] == nifty_index_data.iloc[1]['open']):
            threading.Thread(target=play_sound).start()

            is_buy = False if nifty_index_data.iloc[0]['open'] < nifty_index_data.iloc[0]['close'] else True
            case = int(input("Nhập trade (1 harf) (2 full): "))
            # if(is_buy and (nifty_index_data.iloc[0]['high'] - nifty_index_data.iloc[0]['open'] > nifty_index_data.iloc[0]['open'] - nifty_index_data.iloc[0]['close'] or nifty_index_data.iloc[0]['close'] - nifty_index_data.iloc[0]['low'] > nifty_index_data.iloc[0]['open'] - nifty_index_data.iloc[0]['close'] )):
            #     case = 2
            # if(is_buy == False and (nifty_index_data.iloc[0]['high'] - nifty_index_data.iloc[0]['close'] > nifty_index_data.iloc[0]['close'] - nifty_index_data.iloc[0]['open'] or nifty_index_data.iloc[0]['open'] - nifty_index_data.iloc[0]['low'] > nifty_index_data.iloc[0]['close'] - nifty_index_data.iloc[0]['open'] )):
            #     case = 2
            data = get_price_older(symbol_exness, mt5.TIMEFRAME_M5)
            if(case == 1 or case == 2):
                if(is_buy):
                    # dua vao nen do
                    sl = data['low']
                    entry = data['open' if case == 1 else 'high']
                    tp = entry + (entry - sl)
                    lot = CalculateLotSize(entry, sl)
                    place_stop(symbol_exness, mt5.ORDER_TYPE_BUY_STOP, lot, round(entry, 3), round(sl, 3), 0.0, margic_number)
                    is_delete_old_order = False
                else:
                    # dua vao nen xanh
                    sl = data['high']
                    entry = data['open' if case == 1 else 'low']
                    tp = entry - (sl - entry)
                    lot = CalculateLotSize(entry, sl)
                    place_stop(symbol_exness, mt5.ORDER_TYPE_SELL_STOP, lot, round(entry, 3), round(sl, 3), 0.0, margic_number)
                    is_delete_old_order = False
                margic_number += 1

            price_check = nifty_index_data.iloc[0]['close']
            
    except:
      print('An exception occurred')


