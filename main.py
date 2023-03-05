import sys

from telethon.sync import TelegramClient
from telethon import functions, types
from config import api_id, api_hash, session


def set_emoji_status(document_id: int):
    client = TelegramClient(session, api_id, api_hash)
    client.start()

    client(functions.account.UpdateEmojiStatusRequest(
        emoji_status=types.EmojiStatus(
            document_id=document_id
        )
    ))


def print_emoji_status(short_name: str):
    client = TelegramClient(session, api_id, api_hash)
    client.start()

    result = client(functions.messages.GetStickerSetRequest(
        stickerset=types.InputStickerSetShortName(
            short_name=short_name
        ),
        hash=0
    ))

    for pack in result.packs:
        emoticon = pack.emoticon

        if len(pack.documents) == 1:
            print(f'{emoticon} - {pack.documents[0]}')
        else:
            print(f'{emoticon}')
            for document_id in pack.documents:
                print(f'└ {document_id}')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print_emoji_status(sys.argv[1])
    else:
        print_emoji_status('EmojiStatus')
