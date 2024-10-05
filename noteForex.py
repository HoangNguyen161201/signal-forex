from mailer import send_mail
from time_handle import fomart_time_to_vn
import re
from data import symbols

# api telegram
api_id = '24104392'
api_hash = '3b479abb8cd0b6970cc33a54335dc4e0'

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
        send_mail('hoanghpang@gmail.com', f'forex signal-{order}', f'{fomart_time_to_vn(msg.date)} - {msg.message}')

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

def WSForexSignalsFREEMsg(msg):
    if isinstance(msg.message, str) and 'tp' in msg.message.lower() and 'sl' in msg.message.lower():        
        order = f'@WSForexSignalsFREE|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def ForexxbluepipsMsg(msg):
    if isinstance(msg.message, str) and 'stop loss' in msg.message.lower():        
        order = f'@Forexxbluepips|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

# win:5, #risk:0
return_msg_dict = {
    # đã check
    '@ForexGoldensignall': forexGoldensignallMsg, # da check
    '@GoldTradesignals11': goldTradesignals11Msg, # da check
    '@goldsignalsvip_S': goldsignalsvipsMsg, # da check
    '@investopediaacadem': investopediaacademMsg, # da check
    'Akeem_the_trader': Akeem_the_traderMsg, # da check
    'USDJP': USDJPMsg, # da check
    'Craig_Percoc0': craigPercoc0Msg, # da check
    'Forexxbluepips': ForexxbluepipsMsg, # da check
    'EasyForexPips': easyForexPipsMsg, # da check

    # chưa rõ lắm
    '@tradewithpatfree': tradewithpatfreeMsg, # chua ro
    '@forexstarteam': forexstarteamMsg, # chua ro
    'WSForexSignalsFREE': WSForexSignalsFREEMsg,
}


