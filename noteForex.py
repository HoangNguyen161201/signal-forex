from mailer import send_mail
from time_handle import fomart_time_to_vn
import re
from data import symbols
from order import create_order

# api telegram
api_id = '24104392'
api_hash = '3b479abb8cd0b6970cc33a54335dc4e0'

def create_order_mt5(msg):
    try:
        print(msg.message)
        pattern = r'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
        matches = re.findall(pattern, msg.message)
        numbers = [num for num in matches if len(num) >= 4]
        numbers = [float(num) for num in numbers ]
        numbers.sort()
        type = 'buy' if 'buy' in msg.message.lower() else 'sell'

        # get price ----------------------------------------------------------------
        price = None
        regex_price = r'((?:\d+[,.\d]*)|(?:\d*[.]\d+))-(?:(\d+[,.\d]*)|(\d*[.]\d+))'
        match_price = re.search(regex_price, msg.message)
        prices = []
        if match_price:
            prices.append(match_price.group(1)), prices.append(match_price.group(2)) 
        prices = [num for num in prices if len(num) >= 4]
        prices = [float(num) for num in prices ]
        if(prices.__len__() > 1):
            price = prices
            numbers.remove(prices[0])
        else:
            price = numbers[1] if type == 'buy' else numbers[numbers.__len__() - 2]

        sl = numbers[0] if type == 'buy' else numbers[numbers.__len__() - 1]
        tp = numbers[2] if type == 'buy' else numbers[numbers.__len__() - 3]
        
        symbol = 'XAUUSDm' if 'gold' in msg.message.lower() else None
        if not symbol:
            for key in symbols:
                symbol_keys = key.split('/')
                if symbol_keys[0].lower() in msg.message.lower() and symbol_keys[1].lower() in msg.message.lower():
                    symbol = symbols.get(key)
                    break
        if(symbol):
            create_order(type, symbol, price, sl, tp)
    except Exception as e:
        print(f"Đã xảy ra một lỗi khi tạo order: {e}")

def write_to_file(file_name, message):
    with open(file_name, 'a') as f:
        f.write(f'{message}\n')

def checkOrderExists(order, file):
    content = ''
    with open(file, 'r') as file:
        content = file.read()
    if order in content:
        return True
    return False

def sendOrder(order, msg):
    if not checkOrderExists(order, './order.txt'):
        write_to_file('./order.txt', order)
        create_order_mt5(msg)
        send_mail('hoangdev161201@gmail.com', f'forex signal-{order}', f'{fomart_time_to_vn(msg.date)} - {msg.message}')

# send mail -------------------------------------------------------------
def tradewithpatfreeMsg(msg):
    if isinstance(msg.message, str) and 'Trade Safely' in msg.message:
        order = f'@tradewithpatfree|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def goldTradesignals11Msg(msg):
    if isinstance(msg.message, str) and 'XAUUSD SELL NOW' in msg.message or 'XAUUSD BUY NOW' in msg.message:
        order = f'@GoldTradesignals11|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def goldsignalsvipsMsg(msg):
    if isinstance(msg.message, str) and 'Tp' in msg.message and 'Sl' in msg.message:
        order = f'@goldsignalsvip_S|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def forexstarteamMsg(msg):
    if isinstance(msg.message, str) and 'tp' in msg.message.lower() and 'sl' in msg.message.lower():        
        order = f'@forexstarteam|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def forexGoldensignallMsg(msg):
    if isinstance(msg.message, str) and 'tp' in msg.message.lower() and 'sl' in msg.message.lower():        
        order = f'@ForexGoldensignall|{msg.id}'
        sendOrder(order, msg)
        return True
    return False


def investopediaacademMsg(msg):
    if isinstance(msg.message, str) and 'tp' in msg.message.lower() and 'sl' in msg.message.lower() and ('sell' in msg.message.lower() or 'buy' in msg.message.lower()):
        order = f'@investopediaacadem|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def goldsignalsprofessorMsg(msg):
    if isinstance(msg.message, str) and ('tp' in msg.message.lower() and 'sl' in msg.message.lower()) or(
        'take profit' in msg.message.lower() and 'stop loss' in msg.message.lower()):
        order = f'@Goldsignalsprofessor|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def GOLDFOREXMT4MT5Msg(msg):
    if isinstance(msg.message, str) and 'tp' in msg.message.lower() and 'sl' in msg.message.lower():        
        order = f'@GOLDFOREXMT4MT5|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def Akeem_the_traderMsg(msg):
    if isinstance(msg.message, str) and 'entry' in msg.message.lower() and ('tp' in msg.message.lower() and 'sl' in msg.message.lower()):
        order = f'@Akeem_the_trader|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def easyForexPipsMsg(msg):
    if isinstance(msg.message, str) and 'tp' in msg.message.lower() and 'sl' in msg.message.lower():        
        order = f'@EasyForexPips|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def USDJPMsg(msg):
    if isinstance(msg.message, str) and 'tp' in msg.message.lower() and 'sl' in msg.message.lower():        
        order = f'@USDJP|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def craigPercoc0Msg(msg):
    if isinstance(msg.message, str) and 'tp' in msg.message.lower() and 'sl' in msg.message.lower():        
        order = f'@Craig_Percoc0|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

# win:5, #risk:0
return_msg_dict = {
    # đã check
    '@ForexGoldensignall': forexGoldensignallMsg, #win: 2 #risk: 1
    'GOLDFOREXMT4MT5': GOLDFOREXMT4MT5Msg, # win:1 #risk:0

    # chưa rõ lắm
    '@tradewithpatfree': tradewithpatfreeMsg,
    '@GoldTradesignals11': goldTradesignals11Msg,
    '@goldsignalsvip_S': goldsignalsvipsMsg, 
    '@forexstarteam': forexstarteamMsg,
    '@investopediaacadem': investopediaacademMsg, #win: 0 #loss:0 #lenh: xausd
    
    # kho nhai do sl to, tp thap
    'Akeem_the_trader': Akeem_the_traderMsg, # win: 0 # loss: 0 # lenh: gbpcad
    'EasyForexPips': easyForexPipsMsg,
    'USDJP': USDJPMsg,
    'Craig_Percoc0': craigPercoc0Msg
}


