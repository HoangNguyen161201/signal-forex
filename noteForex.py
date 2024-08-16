from mailer import send_mail
from time_handle import fomart_time_to_vn
from ring import play_ring

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
        send_mail('hoangdev161201@gmail.com', f'forex signal-{order}', f'{fomart_time_to_vn(msg.date)} - {msg.message}')
        play_ring()

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

def wallStreetForexMsg(msg):
    if isinstance(msg.message, str) and 'tp' in msg.message.lower() and 'sl' in msg.message.lower():        
        order = f'@WallStreetForex_Signals|{msg.id}'
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

return_msg_dict = {
    # đã check
    '@WallStreetForex_Signals': wallStreetForexMsg,
    '@ForexGoldensignall': forexGoldensignallMsg,
    
    # chưa rõ lắm
    '@tradewithpatfree': tradewithpatfreeMsg,
    '@GoldTradesignals11': goldTradesignals11Msg,
    '@goldsignalsvip_S': goldsignalsvipsMsg, 
    '@forexstarteam': forexstarteamMsg,
    '@investopediaacadem': investopediaacademMsg,

    'Goldsignalsprofessor': goldsignalsprofessorMsg,
    'GOLDFOREXMT4MT5': GOLDFOREXMT4MT5Msg,

    # kho nhai do sl to, tp thap
    'Akeem_the_trader': Akeem_the_traderMsg


}
