from telethon.sync import TelegramClient
from noteForex import api_id, api_hash
import re
from data import symbols
from order import create_order

client = TelegramClient('session_name', api_id, api_hash)

async def get_message(id_room):
    await client.start()
    async for msg in client.iter_messages(id_room, limit=200):
        if isinstance(msg.message, str) and 'tp' in msg.message.lower() and 'sl' in msg.message.lower():
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
                    break
            except Exception as e:
                print(f"Đã xảy ra một lỗi khi tạo order: {e}")



with client:
    client.loop.run_until_complete(get_message('Craig_Percoc0'))