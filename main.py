from telethon.sync import TelegramClient
from data import api_id, api_hash, return_msg_dict

client = TelegramClient('session_name', api_id, api_hash)

async def get_message(id_room):
    await client.start()
    message = ''
    async for msg in client.iter_messages(id_room, limit=200):
        data = return_msg_dict.get(id_room)(msg)
        if data:
            message = data
            break
    print(message)


    


with client:
    for item in return_msg_dict.keys():
        client.loop.run_until_complete(get_message(item))