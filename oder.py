import MetaTrader5 as mt5
from datetime import datetime, timedelta

def place_order( symbol, type, lot, stop_price, stop_loss, take_profit, magic_number=234000, deviation=10):
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

    # Tạo yêu cầu lệnh
    order_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": type,
        "price": stop_price,
        "sl": stop_loss,
        "tp": take_profit,
        "deviation": deviation,
        "magic": magic_number,
        "type_time": mt5.ORDER_TIME_GTC, 
        "type_filling": mt5.ORDER_FILLING_IOC,
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
        data['open'] = previous_candle['open'] 
        data['high'] = previous_candle['high'] 
        data['low'] = previous_candle['low']  
        data['close'] = previous_candle['close']

    # Đóng kết nối
    mt5.shutdown()

    if(not data['open']):
        return None
    return data

def CalculateLotSize( entry_price, stop_loss_price, distance_check):

    distance = abs(entry_price - stop_loss_price)
    lot = round(((distance_check / distance) *0.02) , 2)
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

def get_current_price(symbol):
    """
    Lấy giá hiện tại (bid và ask) của một tài sản.
    
    :param symbol: Tên tài sản (symbol).
    :return: Từ điển chứa giá bid, ask, và last price hoặc None nếu thất bại.
    """
    # Khởi động MetaTrader 5
    if not mt5.initialize():
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return None

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(79431100, "Cuem161201@", "Exness-MT5Trial8"):
        print(f"Đăng nhập thất bại, lỗi: {mt5.last_error()}")
        mt5.shutdown()
        return None

    # Lấy thông tin giá của tài sản
    tick_info = mt5.symbol_info_tick(symbol)
    if tick_info is None:
        print(f"Không thể lấy giá cho tài sản: {symbol}")
        mt5.shutdown()
        return None

    # Lấy giá bid, ask và last price
    data = {
        "bid": tick_info.bid,
        "ask": tick_info.ask,
        "last": tick_info.last
    }

    # Đóng MetaTrader 5
    mt5.shutdown()
    
    return data


def close_position(magic):
    # Khởi động MetaTrader 5
    if not mt5.initialize():
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return False

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(79431100, "Cuem161201@", "Exness-MT5Trial8"):
        print("Lỗi khi đăng nhập vào tài khoản giao dịch:", mt5.last_error())
        mt5.shutdown()
        return False
    
    # Lấy danh sách tất cả các lệnh mở
    positions = mt5.positions_get()

    if positions is None:
        print("Không có lệnh nào đang mở")
        mt5.shutdown()
        quit()

    # Duyệt qua tất cả các lệnh và đóng nếu magic number phù hợp
    for position in positions:
        if position.magic == magic:

            symbol = position.symbol
            volume = position.volume
            position_id = position.ticket
            price = mt5.symbol_info_tick(symbol).bid if position.type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask
            order_type = mt5.ORDER_TYPE_SELL if position.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY

            # Tạo yêu cầu đóng lệnh
            close_request = {
                "action": mt5.TRADE_ACTION_DEAL,  # Hành động giao dịch
                "symbol": symbol,                 # Cặp tiền
                "volume": volume,                 # Khối lượng
                "type": order_type,               # Loại lệnh ngược
                "position": position_id,          # ID lệnh cần đóng
                "price": price,                   # Giá hiện tại
                "deviation": 10,                  # Độ lệch cho phép
                "magic": magic,            # Magic number
                "comment": "Đóng lệnh theo magic number"
            }
            # Gửi yêu cầu đóng lệnh
            mt5.order_send(close_request)
            
    # Ngắt kết nối MetaTrader 5
    mt5.shutdown()
