import MetaTrader5 as mt5

def trade_request_current(type, sl, tp, symbol, price):
    return {
        "action": mt5.TRADE_ACTION_DEAL,  # Market Order
        "symbol": symbol,
        "volume": 0.01,
        "type":  mt5.ORDER_TYPE_BUY if type == 'buy' else mt5.ORDER_TYPE_SELL ,
        "price": price,
        "sl": sl,
        "tp": tp,
        "deviation": 10,
        "magic": 234000,
        "comment": "Python script Market order",
        "type_time": mt5.ORDER_TIME_GTC, 
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

def trade_request_pending(type, sl, tp, symbol, price):
    return {
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

    trade_request = None
    if isinstance(price, list):
        price_current = mt5.symbol_info_tick(symbol).ask if type == 'buy' else mt5.symbol_info_tick(symbol).bid
        price.sort()
        print(price_current)
        if(price_current >= price[0] and price_current <= price[1]):
            trade_request = trade_request_current(type, sl, tp, symbol, price_current)
        else:
            # price_peding = (price[0] + (price[1] - price[0]) * 0.2) if type == 'buy' else (price[0] + (price[1] - price[0]) * 0.8)
            price_peding = price[1] if type == 'buy' else price[0]
            trade_request = trade_request_pending(type, sl, tp, symbol, price_peding)
    else:
        price_current = mt5.symbol_info_tick(symbol).ask if type == 'buy' else mt5.symbol_info_tick(symbol).bid
        trade_request = trade_request_current(type, sl, tp, symbol,  price_current)

    if(trade_request):
        # Gửi lệnh
        result = mt5.order_send(trade_request)

        # Kiểm tra kết quả
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(result)
            print(f"Order failed, retcode={result.retcode}")
        else:
            print(f"order thành công: {result}")
    else:
        print(f"không có option request")