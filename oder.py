import MetaTrader5 as mt5
from datetime import datetime, timedelta

path = r'C:\Program Files\RoboForex MT5 Terminal\terminal64.exe'

symbols = [
    {
        'symbol_capital': 'Gold',
        'symbol_robo': 'XAUUSD',
        'current_price_file': 'GOLD.csv',
        'two_candle_price_old_file': 'GOLD_5m.csv',
    },
    {
        'symbol_capital': 'US30',
        'symbol_robo': '.US30Cash',
        'current_price_file': 'US30.csv',
        'two_candle_price_old_file': 'US30_5m.csv', 
    },
    {
        'symbol_capital': 'US100',
        'symbol_robo': '.USTECHCash',
        'current_price_file': 'US100.csv',
        'two_candle_price_old_file': 'US100_5m.csv',
    },
    {
        'symbol_capital': 'DE40',
        'symbol_robo': '.DE40Cash',
        'current_price_file': 'GERMANY40.csv',
        'two_candle_price_old_file': 'GERMANY40_5m.csv',
    },
    {
        'symbol_capital': 'EURUSD',
        'symbol_robo': 'EURUSD',
        'current_price_file': 'EURUSD.csv',
        'two_candle_price_old_file': 'EURUSD_5m.csv',
    },
    {
        'symbol_capital': 'USDJPY',
        'symbol_robo': 'USDJPY',
        'current_price_file': 'USDJPY.csv',
        'two_candle_price_old_file': 'USDJPY_5m.csv',
    },
    {
        'symbol_capital': 'EURJPY',
        'symbol_robo': 'EURJPY',
        'current_price_file': 'EURJPY.csv',
        'two_candle_price_old_file': 'EURJPY_5m.csv',
    },
    {
        'symbol_capital': 'GBPJPY',
        'symbol_robo': 'GBPJPY',
        'current_price_file': 'GBPJPY.csv',
        'two_candle_price_old_file': 'GBPJPY_5m.csv',
    },
    {
        'symbol_capital': 'GBPUSD',
        'symbol_robo': 'GBPUSD',
        'current_price_file': 'GBPUSD.csv',
        'two_candle_price_old_file': 'GBPUSD_5m.csv',
    },
]

def place_order(symbol, type, lot, stop_price, stop_loss, take_profit, magic_number=234000, deviation=10):
    # Khởi động MetaTrader 5
    if not mt5.initialize(path):
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return False

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(67138737, "Cuem161201@", "RoboForex-ECN"):
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
    if not mt5.initialize(path):
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return False

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(67138737, "Cuem161201@", "RoboForex-ECN"):
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
        "type_time": mt5.ORDER_TIME_DAY, 
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

def get_price_older(symbol, timeframe, number_candle):    
    mt5.initialize(path)

    data = {}

    if not mt5.login(67138737, "Cuem161201@", "RoboForex-ECN"):
        print(f"Đăng nhập thất bại, lỗi: {mt5.last_error()}")
    else:
        print("Đăng nhập thành công!")

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, number_candle)

    if rates is not None and len(rates) > 1:
        previous_candle = rates[0]
        data['open'] = previous_candle['open'] 
        data['high'] = previous_candle['high'] 
        data['low'] = previous_candle['low']  
        data['close'] = previous_candle['close']

    # Đóng kết nối
    mt5.shutdown()

    if(not data['open']):
        return None
    return data

# Kết nối tới MetaTrader 5
if not mt5.initialize(path):
    print("Lỗi khi kết nối tới MetaTrader 5")
    mt5.shutdown()
    quit()

def close_order_by_magic_number(magic_number):
    # Khởi động MetaTrader 5
    if not mt5.initialize(path):
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return False

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(67138737, "Cuem161201@", "RoboForex-ECN"):
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
    if not mt5.initialize(path):
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return None

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(67138737, "Cuem161201@", "RoboForex-ECN"):
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
    if not mt5.initialize(path):
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return False

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(67138737, "Cuem161201@", "RoboForex-ECN"):
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


def calculate_lots(riskPercent, lDistance, symbol):
    if not mt5.initialize(path):
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return False

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(67138737, "Cuem161201@", "RoboForex-ECN"):
        print("Lỗi khi đăng nhập vào tài khoản giao dịch:", mt5.last_error())
        mt5.shutdown()
        return False
    
    # Get required symbol properties
    ticksize = mt5.symbol_info(symbol).trade_tick_size
    tickvalue = mt5.symbol_info(symbol).trade_tick_value
    lotstep = mt5.symbol_info(symbol).volume_step
    
    # Check if the values are valid
    if ticksize == 0 or tickvalue == 0 or lotstep == 0:
        print("Lot size cannot be calculated due to invalid values.")
        return 0
    
    # Get the account balance
    account_balance = mt5.account_info().balance
    
    # Calculate risk money
    riskMoney = account_balance * riskPercent / 100
    
    # Calculate money per lotstep
    moneyLotstep = (lDistance / ticksize) * tickvalue * lotstep
    
    # Calculate the lot size
    lots = riskMoney / moneyLotstep
    
    # Ensure the lot size is rounded down to the nearest valid lot step
    lots = int(lots // lotstep) * lotstep * 0.01
    
    return round(lots, 2)


def get_info_position(magic_number, symbol):
    # Khởi tạo MetaTrader 5
    if not mt5.initialize():
        print("Lỗi khi khởi tạo MetaTrader5:", mt5.last_error())
        return None

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(67138737, "Cuem161201@", "RoboForex-ECN"):
        print("Lỗi khi đăng nhập vào tài khoản giao dịch:", mt5.last_error())
        mt5.shutdown()
        return None

    # Lấy danh sách các vị thế mở
    positions = mt5.positions_get(symbol=symbol)
    if positions is None or len(positions) == 0:
        print("Không có vị thế mở cho symbol:", symbol)
        mt5.shutdown()
        return None

    # Tìm vị thế khớp với magic_number
    for position in positions:
        if position.magic == magic_number:
            mt5.shutdown()
            return {
                "ticket": position.ticket,
                "price_open": position.price_open,
                "sl": position.sl,
                "tp": position.tp,
            }

    # Nếu không tìm thấy vị thế khớp
    mt5.shutdown()
    return None

def update_stop_loss(magic_number, symbol, sl = None, tp = None):
    is_success = True
    if not mt5.initialize(path):
        print("Lỗi khi khởi tạo MetaTrader5", mt5.last_error())
        return False

    # Đăng nhập vào tài khoản giao dịch
    if not mt5.login(67138737, "Cuem161201@", "RoboForex-ECN"):
        print("Lỗi khi đăng nhập vào tài khoản giao dịch:", mt5.last_error())
        mt5.shutdown()
        return False

    # Lấy danh sách các vị thế mở
    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        print("Không có vị thế mở cho symbol:", symbol)
        mt5.shutdown()
        return False

    for position in positions:
        # Kiểm tra magic number
        if position.magic == magic_number:
            ticket = position.ticket
            price_open = position.price_open  # Giá mở vị thế ban đầu

            # Gửi lệnh cập nhật SL
            request = {
                "action": mt5.TRADE_ACTION_SLTP,
                "symbol": symbol,
                "position": ticket,
                "sl": price_open if sl is None else sl,  # Cập nhật Stop Loss
                "tp": position.tp if tp is None else tp,  # Giữ nguyên Take Profit (nếu có)
                "magic": magic_number
            }
            result = mt5.order_send(request)


    
    # Đóng MetaTrader5
    mt5.shutdown()
    return is_success

# place_order('XAUUSD', mt5.ORDER_TYPE_BUY, 0.01, 0.0, 0.0, 0.0, 1122)
# update_stop_loss(1122, 'XAUUSD', 2500.00, 2700.00)