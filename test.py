from telethon.sync import TelegramClient
from noteForex import api_id, api_hash

client = TelegramClient('session_name', api_id, api_hash)

async def get_message(id_room):
    await client.start()
    async for msg in client.iter_messages(id_room, limit=200):
        if isinstance(msg.message, str) and 'entry' in msg.message.lower() and ('tp' in msg.message.lower() and 'sl' in msg.message.lower()):
            print(msg.message)


    


with client:
    client.loop.run_until_complete(get_message('Akeem_the_trader'))