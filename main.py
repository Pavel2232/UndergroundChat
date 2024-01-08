import asyncio
import datetime

import aiofiles


async def write_message_file(message):
    async with aiofiles.open('chat', mode='a') as f:
        await f.write(message)


async def tcp_client():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)

    while True:
        data_chanel = await reader.readline()
        date = f'[{datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}] '
        log_message = date + data_chanel.decode()
        await write_message_file(log_message)
        print(f'{log_message}')


asyncio.run(tcp_client())
