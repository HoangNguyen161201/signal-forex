from telethon.sync import TelegramClient
from noteForex import api_id, api_hash, return_msg_dict

client = TelegramClient('session_name', api_id, api_hash)

async def get_message(id_room):
    await client.start()
    message = ''
    async for msg in client.iter_messages(id_room, limit=100):
        if ('tp' in msg.message.lower() and 'sl' in msg.message.lower()) and ('limit' in msg.message.lower() or 'now' in msg.message.lower()):
            print(msg.message)


    


with client:
    client.loop.run_until_complete(get_message('gfr_smc_analysis'))