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

def play_sound():  
    mixer.init()
    mixer.music.load('./ring.mp3')
    mixer.music.play()

while True:
    try:
        tv = TvDatafeed()
        nifty_index_data = tv.get_hist(symbol= symbol_tradingview,exchange='CAPITALCOM',interval=Interval.in_1_minute,n_bars=2)
        print(f'{nifty_index_data.iloc[0]['close']}-{nifty_index_data.iloc[1]['open']}')
        if(price_check != nifty_index_data.iloc[0]['close'] and nifty_index_data.iloc[0]['close'] == nifty_index_data.iloc[1]['open']):
            threading.Thread(target=play_sound).start()

            old_is_buy = is_buy
            is_buy = False if nifty_index_data.iloc[0]['open'] < nifty_index_data.iloc[0]['close'] else True
            
            case = int(input(f"trade {'buy' if is_buy else 'sell'} (1- nữa cây nến | 2 - full cây nến): "))
            data = get_price_older(symbol_exness, mt5.TIMEFRAME_M1)
            if(case == 1 or case == 2):
                if(is_buy):
                    # dua vao nen do
                    sl = data['low']
                    entry = data['open' if case == 1 else 'high']
                    tp = entry + (entry - sl)
                    lot = CalculateLotSize(entry, sl)
                    place_stop(symbol_exness, mt5.ORDER_TYPE_BUY_STOP, lot, round(entry, 3), round(sl, 3), round(tp, 3), margic_number)
                else:
                    # dua vao nen xanh
                    sl = data['high']
                    entry = data['open' if case == 1 else 'low']
                    tp = entry - (sl - entry)
                    lot = CalculateLotSize(entry, sl)
                    place_stop(symbol_exness, mt5.ORDER_TYPE_SELL_STOP, lot, round(entry, 3), round(sl, 3), round(tp, 3), margic_number)
                
                if(old_is_buy == is_buy):
                    close_order_by_magic_number(margic_number - 1)
                    print("đã đóng lệnh")
                margic_number += 1
                print("đã vào lệnh")
                
                
            price_check = nifty_index_data.iloc[0]['close']
            
    except:
      print('An exception occurred')


