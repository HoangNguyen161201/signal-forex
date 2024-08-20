from telethon.sync import TelegramClient
from noteForex import api_id, api_hash
import re
from data import symbols
from order import create_order

client = TelegramClient('session_name', api_id, api_hash)

async def get_message(id_room):
    await client.start()
    async for msg in client.iter_messages(id_room, limit=200):
        if isinstance(msg.message, str) and 'entry' in msg.message.lower() and ('tp' in msg.message.lower() and 'sl' in msg.message.lower()):
            pattern = r'\b\d+\.\d+\b'
            matches = re.findall(pattern, msg.message)
            numbers = [num for num in matches if len(num) >= 4]
            numbers = [float(num) for num in numbers ]
            numbers.sort()
            type = 'buy' if 'buy' in msg.message.lower() else 'sell'
            sl = numbers[0] if type == 'buy' else numbers[numbers.__len__() - 1]
            price = numbers[1] if type == 'buy' else numbers[numbers.__len__() - 2]
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



with client:
    client.loop.run_until_complete(get_message('Akeem_the_trader'))