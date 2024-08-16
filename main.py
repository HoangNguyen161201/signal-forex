from telethon.sync import TelegramClient
from noteForex import api_id, api_hash, return_msg_dict
import time

client = TelegramClient('session_name', api_id, api_hash)

async def get_message(id_room):
    await client.start()
    async for msg in client.iter_messages(id_room, limit=30):
        data = return_msg_dict.get(id_room)(msg)
        if data:
            break

loop = 1
while True:
    with client:
        for item in return_msg_dict.keys():
            client.loop.run_until_complete(get_message(item))
    loop += 1
    time.sleep(1)
    print(f'loop {loop}')