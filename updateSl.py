import MetaTrader5 as mt5

def updare_sl(symbol, timeframe):
     # Khởi động MetaTrader 5
    if not mt5.initialize():
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return False

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(79431100, "Cuem161201@", "Exness-MT5Trial8"):
        print("Lỗi khi đăng nhập vào tài khoản giao dịch:", mt5.last_error())
        mt5.shutdown()
        return False

    # Lấy tất cả các lệnh mở
    positions = mt5.positions_get()

    # Kiểm tra xem có lệnh nào không
    if positions is None:
        print("Không có vị trí mở nào.")    
    else:
        
        for position in positions:
            ticket = position.ticket
            entry_price = position.price_open
            sl = position.sl
            comment = position.comment

            if comment:               
                rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1)
                current_price = 0
                sl_initial = float(comment)
                is_buy =  True if sl_initial < entry_price else False
                if rates is not None:
                    previous_candle = rates[0]
                    current_price = previous_candle['high' if is_buy else 'low']   # Giá mở cửa

                
                if(((is_buy and sl < entry_price) or (not is_buy and sl > entry_price) ) and abs(current_price - entry_price) > abs(entry_price - sl_initial)/ 2):
                    request = {
                        "action": mt5.TRADE_ACTION_SLTP,
                        "symbol": symbol,
                        "position": ticket,
                        "sl": entry_price,
                    }

                    mt5.order_send(request)
                  

                if((is_buy and sl >= entry_price) or (not is_buy and sl <= entry_price)):
                    sl =  round(sl + abs(entry_price - sl_initial) if is_buy else sl - abs(entry_price - sl_initial), 3)
                    if((is_buy and sl < current_price - abs(entry_price - sl_initial)) or not is_buy and sl > current_price + abs(entry_price - sl_initial)):
                        request = {
                            "action": mt5.TRADE_ACTION_SLTP,
                            "symbol": symbol,
                            "position": ticket,
                            "sl": sl,
                        }

                        mt5.order_send(request)
                        print(f'Đã cập nhật SL 2')

    # Đóng kết nối MT5
    mt5.shutdown()

print('start')
while True:
    updare_sl('XAUUSD', mt5.TIMEFRAME_M1)
