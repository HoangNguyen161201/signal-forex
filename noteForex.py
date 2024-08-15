from mailer import send_mail
from time_handle import fomart_time_to_vn

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

# send mail -------------------------------------------------------------
def tradewithpatfreeMsg(msg):
    if 'Trade Safely' in msg.message:
        order = f'@tradewithpatfree|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def goldTradesignals11Msg(msg):
    if 'XAUUSD SELL NOW' in msg.message or 'XAUUSD BUY NOW' in msg.message:
        order = f'@GoldTradesignals11|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def goldsignalsvipsMsg(msg):
    if 'Tp' in msg.message and 'Sl' in msg.message:
        order = f'@goldsignalsvip_S|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def forexstarteamMsg(msg):
    if 'tp' in msg.message.lower() and 'sl' in msg.message.lower():        
        order = f'@forexstarteam|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def forexGoldensignallMsg(msg):
    if 'tp' in msg.message.lower() and 'sl' in msg.message.lower():        
        order = f'@ForexGoldensignall|{msg.id}'
        sendOrder(order, msg)
        return True
    return False

def wallStreetForexMsg(msg):
    if 'tp' in msg.message.lower() and 'sl' in msg.message.lower():        
        order = f'@WallStreetForex_Signals|{msg.id}'
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
}
