from telethon.sync import TelegramClient
from telethon import functions, types
from flask import abort
from config import api_hash, api_id, session
import asyncio

STATUS = {
    "busy": 5812416496223129240,
    "online": 5810051751654460532,
    "offline": 5807786710456602258
}

def get_emoji_status():

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    client = TelegramClient(session, api_id, api_hash, loop=loop)
    
    client.start()

    result = client(functions.users.GetFullUserRequest(
        id='tinitun'
    ))

    client.disconnect()
    document_id = int(result.users[0].emoji_status.document_id)

    reverseMap = dict(zip(STATUS.values(), STATUS.keys()))
    res = reverseMap.get(document_id)

    return {"document_id": str(document_id), "status_name": res}

def put_emoji_status(status):
    status_name = status.get("status_name")

    if status_name in STATUS:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient(session, api_id, api_hash)
        client.start()

        client(functions.account.UpdateEmojiStatusRequest(
            emoji_status=types.EmojiStatus(
                document_id=STATUS[status_name]
            )
        ))
        client.disconnect()
        return {"status": STATUS[status_name]}
    else:
        abort(404, f"Status with status name {status_name} is not found")
