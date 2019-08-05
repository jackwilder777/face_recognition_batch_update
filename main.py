import sys

if len(sys.argv) < 2:
    print("python3 {} <target folder>".format(sys.argv[0]))
    exit(1)

import os
import time
import asyncio
from telethon import errors
from telethon import functions, types
from telethon import TelegramClient
import zipfile

DELAY = 0.5
FETCH_DELAY = 0.5
BOT_ID = '@FILL_ME_IN_BEFORE_USE!'

try:
    api_id = None
    api_hash = None
    FILENAME = 'user'
    SESSION = FILENAME
    exec(open('credential.py').read())
except IOError:
    print("Cannot open session file")
    exit(1)

async def send_message(client, entity, message):
    sent_message = await client.send_message(entity, message)
    return sent_message.id

async def send_photo(client, entity, photo):
    sent_photo = await client.send_file(entity, file=photo)
    return sent_photo.id

async def get_messages(client, entity, last_id):
    messages = []
    async for message in client.iter_messages(entity):
        if message.id > last_id:
            messages.append(message)
        else:
            break
    return messages

async def fetch_message(client, entity, last_id, count):
    messages = []
    while True:
        if len(messages) == count:
            return messages
        messages = await get_messages(client, entity, last_id)
        time.sleep(FETCH_DELAY)

def get_file_paths(folder_path):
    all_paths = []
    file_names = []
    for file_name in os.listdir(folder_path):
        ext = file_name[-3:]
        ext2 = file_name[-4:]
        if not ext in ['jpg', 'png'] and ext2 != 'jpeg':
            continue
        if file_name[0] == '.':
            continue
        file_path = os.path.join(folder_path + '/' + file_name)
        all_paths.append(file_path)
        file_names.append(file_name)
    return all_paths, file_names

async def main():
    client = await TelegramClient(SESSION, api_id, api_hash).start()
    entity = await client.get_entity(BOT_ID)
    file_paths, file_names = get_file_paths(sys.argv[1])
    outfile = open('result.txt', 'w')
    # In case if there's any state
    last_id = await send_message(client, entity, '/done')
    # Wait for done signal
    await fetch_message(client, entity, last_id, 1)
    for file_path, file_name in zip(file_paths, file_names):
        if file_name[-4:] == 'jpeg':
            # Remove file extension
            command = '/train {}'.format(file_name[:-5])
        else:
            # Remove file extension
            command = '/train {}'.format(file_name[:-4])
        # Remove dupliation indicator
        if command[-2:-1] == '_':
            command = command[:-2]
        # Send train command
        last_id = await send_message(client, entity, command)
        # Wait for train signal
        await fetch_message(client, entity, last_id, 1)
        # Send photo
        photo = open(file_path, 'rb')
        last_id = await send_photo(client, entity, photo)
        # Wait for photo received signal
        await fetch_message(client, entity, last_id, 1)
        # Done training current label
        last_id = await send_message(client, entity, '/done')
        # Wait for done signal
        await fetch_message(client, entity, last_id, 1)
        print(file_path)
        outfile.write(file_path + '\n')
        time.sleep(DELAY)
    
    outfile.close()

asyncio.get_event_loop().run_until_complete(main())
