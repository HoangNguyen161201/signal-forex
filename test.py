from oder import place_stop, get_price_older, CalculateLotSize, close_order_by_magic_number, place_order
import MetaTrader5 as mt5

place_order('BTCUSD', mt5.ORDER_TYPE_BUY, 0.01, 0.0, 89308.0, 91947.0)