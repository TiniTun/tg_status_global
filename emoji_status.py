from telethon import TelegramClient
from telethon import functions, types
from telethon.sessions import StringSession
from flask import abort
from config import api_hash, api_id, session
import asyncio

STATUS = {
    "busy": 5812416496223129240,
    "online": 5810051751654460532,
    "offline": 5807786710456602258
}

#loop = asyncio.new_event_loop()
#asyncio.set_event_loop(loop)
loop = asyncio.get_event_loop()
client = TelegramClient(StringSession(session), api_id, api_hash, loop=loop)

def get_emoji_status():
    return loop.run_until_complete(_get_emoji_status())

async def _get_emoji_status():
    
    await client.start()
    
    result = await client(functions.users.GetFullUserRequest(
        id='tinitun'
    ))

    await client.disconnect()
    document_id = int(result.users[0].emoji_status.document_id)

    reverseMap = dict(zip(STATUS.values(), STATUS.keys()))
    res = reverseMap.get(document_id)

    return {"document_id": str(document_id), "status_name": res}

def put_emoji_status(status):
        return loop.run_until_complete(_put_emoji_status(status))

async def _put_emoji_status(status):
    status_name = status.get("status_name")

    if status_name in STATUS:
        
        await client.start()

        await client(functions.account.UpdateEmojiStatusRequest(
            emoji_status = types.EmojiStatus(
                document_id = STATUS[status_name]
            )
        ))
        await client.disconnect()
        return {"status": STATUS[status_name]}
    else:
        abort(404, f"Status with status name {status_name} is not found")
