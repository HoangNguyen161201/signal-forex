import MetaTrader5 as mt5
from datetime import datetime, timedelta

def place_stop( symbol, type, lot, stop_price, stop_loss, take_profit, magic_number=234000, deviation=10):
    # Khởi động MetaTrader 5
    if not mt5.initialize():
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return False

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(79431100, "Cuem161201@", "Exness-MT5Trial8"):
        print("Lỗi khi đăng nhập vào tài khoản giao dịch:", mt5.last_error())
        mt5.shutdown()
        return False

    # Kiểm tra thông tin về tài sản (symbol)
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Không tìm thấy thông tin về {symbol}")
        mt5.shutdown()
        return False

    # Nếu thị trường của tài sản chưa bật, bật nó lên
    if not symbol_info.visible:
        print(f"{symbol} chưa được bật, bật tài sản lên")
        mt5.symbol_select(symbol, True)

    current_time = datetime.now().replace(second=0, microsecond=0)
    expiration_time = current_time + timedelta(minutes=10)

    # Tạo yêu cầu lệnh
    order_request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": lot,
        "type": type,
        "price": stop_price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": deviation,
        "magic": magic_number,
        "type_time": mt5.ORDER_TIME_SPECIFIED, 
        "type_filling": mt5.ORDER_FILLING_IOC,
        "expiration": int(expiration_time.timestamp()),
        "comment": f'{stop_loss}',
    }

    # Gửi yêu cầu lệnh
    result = mt5.order_send(order_request)

    print(result)
    # Kiểm tra kết quả
    if result == None:
        print(f"Lỗi khi đặt lệnh: {result}")
        mt5.shutdown()
        return False

    print(f"Lệnh Stop đã được đặt thành công, ticket: {result.order}")
    
    # Tắt MetaTrader 5
    mt5.shutdown()
    return True

def get_price_older(symbol, timeframe):    
    mt5.initialize()

    data = {}

    if not mt5.login(79431100, "Cuem161201@", "Exness-MT5Trial8"):
        print(f"Đăng nhập thất bại, lỗi: {mt5.last_error()}")
    else:
        print("Đăng nhập thành công!")
    n_candles = 2

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, n_candles)

    if rates is not None and len(rates) > 1:
        previous_candle = rates[-2]
        data['open'] = previous_candle['open']   # Giá mở cửa
        data['high'] = previous_candle['high']   # Giá cao
        data['low'] = previous_candle['low']     # Giá thấp
        data['close'] = previous_candle['close'] # Giá đóng cửa

    # Đóng kết nối
    mt5.shutdown()

    if(not data['open']):
        return None
    return data

def CalculateLotSize( entry_price, stop_loss_price):

    distance = abs(entry_price - stop_loss_price)
    lot = round(((1 / distance) *0.02) , 2)
    if(lot <= 0.01):
      lot = 0.01
    
    if(lot >= 200):
      lot = 190

    return lot


import MetaTrader5 as mt5

# Kết nối tới MetaTrader 5
if not mt5.initialize():
    print("Lỗi khi kết nối tới MetaTrader 5")
    mt5.shutdown()
    quit()

def close_order_by_magic_number(magic_number):
    # Khởi động MetaTrader 5
    if not mt5.initialize():
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return False

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(79431100, "Cuem161201@", "Exness-MT5Trial8"):
        print("Lỗi khi đăng nhập vào tài khoản giao dịch:", mt5.last_error())
        mt5.shutdown()
        return False
    
    orders = mt5.orders_get()
    if orders is None:
        print("Không thể lấy danh sách lệnh chờ")
        return

    # Lọc các lệnh Buy Stop theo magic number
    for order in orders:
        if order.magic == magic_number:
            # Tạo yêu cầu hủy lệnh
            request = {
                "action": mt5.TRADE_ACTION_REMOVE,
                "order": order.ticket,
            }
            mt5.order_send(request)
            # Gửi yêu cầu hủy lệnh
            print("đóng lệnh thành công")
    
    # Tắt MetaTrader 5
    mt5.shutdown()
