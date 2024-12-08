from pygame import mixer  # Load the popular external library
from oder import close_position, place_order, calculate_lots, update_stop_loss, get_info_position
import MetaTrader5 as mt5
import threading
from datetime import datetime
import pytz
import csv
import time
from data import SymboInfoTrade
from oder import symbols

lock = threading.Lock()

#info
index = int(input('nhập tên index symbol (0 - 7):'))
current_price_path = rf'C:\Users\hoang\AppData\Roaming\MetaQuotes\Terminal\B3FBDE368DD9733D40FCC49B61D1B808\MQL4\Files\{symbols[index]['current_price_file']}'
two_candle_price_path = rf'C:\Users\hoang\AppData\Roaming\MetaQuotes\Terminal\B3FBDE368DD9733D40FCC49B61D1B808\MQL4\Files\{symbols[index]['two_candle_price_old_file']}'
symbol_trade = symbols[index]['symbol_robo']
symbol_check_price = symbols[index]['symbol_capital']


# thay đổi
info_checks = []
info_trades = []
price_check = 0

print("start")

# Lấy thời gian hiện tại
def get_random_number(): 
    current_time = time.time()
    random_number = int(current_time * 1000) % 100000
    return random_number

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

def check():
    global price_check, info_checks
    while True:
        try:
            candle_1_state = None
            candle_2_state = None 

            with open(two_candle_price_path, mode="r") as file:
                reader = csv.reader(file)
                first_row = next(reader)
                first_value = first_row[0]
                if(first_value):
                    data = first_value.split(';')
                    candle_1_state = {
                        'open':  float(data[0]),
                        'close':  float(data[1]),
                        'high': float(data[2]),
                        'low': float(data[3]),
                    }
                    candle_2_state = {
                        'open':  float(data[4]),
                        'close':  float(data[5]),
                        'high': float(data[6]),
                        'low': float(data[7]),
                    }

            is_buy_1 = False if candle_1_state['open'] > candle_1_state['close'] else True
            is_buy_2 = False if candle_2_state['open'] > candle_2_state['close'] else True

            if(candle_1_state is not None and price_check != candle_1_state['close']):
                if(is_buy_1 and not is_buy_2):
                    body_1 = candle_1_state['close'] - candle_1_state['open']
                    body_2 = candle_2_state['open'] - candle_2_state['close']
                    if(body_2 <= body_1 / 2 and candle_2_state['low'] > candle_1_state['open']):
                        lot = calculate_lots(
                            1,
                            abs((candle_1_state['high'] if candle_1_state['high'] > candle_2_state['high'] else candle_2_state['high']) - candle_2_state['low']),
                            symbol_trade
                            )
                        text = f"{symbol_trade}-buy-{lot}"
                    
                        info_checks.append(SymboInfoTrade(candle_1_state,candle_2_state,lot, True))
                        edit_file(text)
                        threading.Thread(target=play_sound).start()
                if(not is_buy_1 and is_buy_2):
                    body_1 = candle_1_state['open'] - candle_1_state['close']
                    body_2 = candle_2_state['close'] - candle_2_state['open']
                    if(body_2 <= body_1 / 2 and candle_2_state['high'] < candle_1_state['open']):
                        lot = calculate_lots(
                            1,
                            abs((candle_1_state['low'] if candle_1_state['low'] < candle_2_state['low'] else candle_2_state['low']) - candle_2_state['high']),
                            symbol_trade
                            )
                        text = f"{symbol_trade}-sell-{lot}"

                        info_checks.append(SymboInfoTrade(candle_1_state,candle_2_state,lot, False))

                        edit_file(text)
                        threading.Thread(target=play_sound).start()
            price_check = candle_1_state['close']
        except:
            t = 1
      

def trade():
    global info_trades, info_checks
    while True:
        try:
            if(info_checks.__len__() > 0):
                print('cập nhật mảng')
                info_trades.extend(info_checks)
                info_checks.clear()
                
            if(info_trades.__len__() > 0):
                best_high = info_trades[0].candle1['high'] if info_trades[0].candle1['high'] > info_trades[0].candle2['high'] else info_trades[0].candle2['high'] 
                best_low = info_trades[0].candle1['low'] if info_trades[0].candle1['low'] < info_trades[0].candle2['low'] else info_trades[0].candle2['low'] 
                
                current_price = 0
                with open(current_price_path, mode="r") as file:
                    reader = csv.reader(file)
                    first_row = next(reader)  # Đọc hàng đầu tiên
                    first_value = first_row[0]
                    if(first_value):
                        current_price = float(first_value)

                for key, info_trade in enumerate(reversed(info_trades)):
                    index_to_delete = len(info_trades) - 1 - key

                    if((info_trade.is_buy and not info_trade.is_hedging and current_price < best_low) or 
                    (not info_trade.is_buy and not info_trade.is_hedging and current_price > best_high)
                    ):
                        print('không trade được vì không đúng điều kiện')
                        info_trades.pop(index_to_delete)
                    else:
                        if(info_trade.is_wait_to_cut and info_trade.magic_1 and info_trade.magic_2):
                            position1 = get_info_position(info_trade.magic_1, symbol_trade)
                            position2 = get_info_position(info_trade.magic_2, symbol_trade)
                            if(position1 is not None and position2 is not None):
                                if(position1['sl'] != 0 and position1['tp'] != 0 and position2['sl'] != 0 and position2['tp'] != 0):
                                    print('đã cập nhật thành công sl và tp cả 2')
                                    info_trades.pop(index_to_delete)
                                else:
                                  
                                    distance = abs(position1['price_open'] - position2['price_open'])
                                    tp1 = position1['price_open']
                                    sl1 = position1['price_open'] - (distance * 2) if info_trade.is_buy else position1['price_open'] + (distance * 2)
                                    tp2 = position2['price_open'] - distance if info_trade.is_buy else position2['price_open'] + distance
                                    sl2 = position1['price_open']
                                    update_stop_loss(info_trade.magic_1, symbol_trade,sl1, tp1 )
                                    update_stop_loss(info_trade.magic_2, symbol_trade, sl2, tp2)
                          
                            

                        if((info_trade.is_buy and not info_trade.is_update_sl and info_trade.is_hedging and current_price >= best_high +((best_high - info_trade.candle2['low'])/2)) or
                        (not info_trade.is_buy and not info_trade.is_update_sl and info_trade.is_hedging and current_price <= best_low -((info_trade.candle2['high'] - best_low)/2))
                        ):
                            print('cập nhật sl')
                            info_trade.setIsUpdateSl(True)
                            update_stop_loss(info_trade.magic_1, symbol_trade)

                        if((info_trade.is_buy and info_trade.is_update_sl and current_price <= best_high) or
                        (not info_trade.is_buy and info_trade.is_update_sl and current_price >= best_low)
                        ):
                            print('hòa vốn')
                            close_position(info_trade.magic_1)
                            info_trades.pop(index_to_delete)
                            
                    
                        if((info_trade.is_buy and info_trade.is_hedging and current_price >= (best_high + (best_high - info_trade.candle2['low']))) or
                        (not info_trade.is_buy and info_trade.is_hedging and current_price <= (best_low - (info_trade.candle2['high'] - best_low)))
                        ):
                            print('cán tp cắt lệnh')
                            close_position(info_trade.magic_1)
                            close_position(info_trade.magic_2)
                            info_trades.pop(index_to_delete)

                        if((info_trade.is_buy and info_trade.is_wait_to_cut and current_price <= info_trade.candle2['low']) or
                        (not info_trade.is_buy and info_trade.is_wait_to_cut and current_price >= info_trade.candle2['high'])
                        ):
                            print('cán hòa cắt lệnh')
                            close_position(info_trade.magic_1)
                            close_position(info_trade.magic_2)
                            info_trades.pop(index_to_delete)
                    
                        if(info_trade.lot > 0 and info_trade.is_buy and info_trade.is_hedging and not info_trade.is_wait_to_cut and current_price <= ((best_high + info_trade.candle2['low']) / 2)):
                            print(f'đánh ngược để cân bằng {info_trade.lot}')
                            info_trade.setMagic(get_random_number(), False)
                            place_order(symbol_trade, mt5.ORDER_TYPE_SELL, info_trade.lot, 0.0, 0.0, 0.0, info_trade.magic_2 )
                            info_trade.setIsWaitToCut(True)
                            
                        if(info_trade.lot > 0 and not info_trade.is_buy and info_trade.is_hedging and not info_trade.is_wait_to_cut and current_price >= ((info_trade.candle2['high'] + best_low) / 2)):
                            print(f'đánh ngược để cân bằng {info_trade.lot}')
                            info_trade.setMagic(get_random_number(), False)
                            place_order(symbol_trade, mt5.ORDER_TYPE_BUY, info_trade.lot, 0.0, 0.0, 0.0, info_trade.magic_2 )
                            info_trade.setIsWaitToCut(True)

                        if(info_trade.is_buy and current_price > best_high and not info_trade.is_hedging and info_trade.lot > 0):
                            print(f'buy nha {info_trade.lot}')
                            info_trade.setMagic(get_random_number(), True)
                            place_order(symbol_trade, mt5.ORDER_TYPE_BUY, info_trade.lot, 0.0, 0.0, 0.0, info_trade.magic_1 )
                            info_trade.setIsHedging(True)
                            info_trade.setLot(info_trade.lot * 2)
                        if(not info_trade.is_buy and current_price < best_low and not info_trade.is_hedging and info_trade.lot > 0):
                            print(f'sell nha {info_trade.lot}')
                            info_trade.setMagic(get_random_number(), True)
                            place_order(symbol_trade, mt5.ORDER_TYPE_SELL, info_trade.lot, 0.0, 0.0, 0.0, info_trade.magic_1 )
                            info_trade.setIsHedging(True)
                            info_trade.setLot(info_trade.lot * 2)
        except:
            t = 1


thread1 = threading.Thread(target=check)
thread2 = threading.Thread(target=trade)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
    