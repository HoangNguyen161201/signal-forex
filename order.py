import MetaTrader5 as mt5


def create_order(type, symbol, price, sl, tp):
    print(type, symbol, price, sl, tp)
    # Kết nối tới MT5
    if not mt5.initialize():
        print("Failed to initialize MT5")
        mt5.shutdown()


    login = 181622838 
    password = "Kingspear1999@" 
    server = "Exness-MT5Trial6" 


    if not mt5.login(login, password, server):
        mt5.shutdown()
    else:
        print(f"Logged in to {server} successfully")


    # Tạo yêu cầu giao dịch BUY limit
    trade_request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": symbol,
        "volume": 0.01,
        "type": mt5.ORDER_TYPE_BUY_LIMIT if type == 'buy' else mt5.ORDER_TYPE_SELL_LIMIT,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "magic": 234000,
        "comment": "Python script BUY limit order",
        "type_time": mt5.ORDER_TIME_GTC, 
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    # Gửi lệnh
    result = mt5.order_send(trade_request)

    # Kiểm tra kết quả
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(result)
        print(f"Order failed, retcode={result.retcode}")
    else:
        print(f"Order placed successfully! Ticket number: {result.order}")