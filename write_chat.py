import asyncio
import json
import logging

import aiofiles

logging.getLogger(__name__)
logging.basicConfig(level=1
                    )


async def submit_message(writer, reader):
    while True:
        user_text = input().rstrip()
        logging.debug(f'Sender: {user_text}')
        writer.write(user_text.encode())
        await writer.drain()

        writer.write('\n'.encode())
        await writer.drain()

        writer.write('\n'.encode())
        await writer.drain()

        data = await reader.read(1000)
        logging.debug(f'Received: {data.decode().rstrip()}')


async def authorisation():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    writer.write('1d1405f0-ae49-11ee-aae7-0242ac110002'.encode())
    await writer.drain()

    writer.write('\n'.encode())
    await writer.drain()

    await reader.read(1000)
    recived = await reader.read(1000)
    print(recived.decode())

    if recived.decode().startswith('\nnull'):
        print('Неизвестный токен. Проверьте его или зарегистрируйте заново.')

    else:
        await submit_message(writer, reader)


async def registration():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    writer.write('\n'.encode())
    await writer.drain()

    data = await reader.read(1000)
    print(f'data: {data.decode()}')

    user_text = input().rstrip()
    logging.debug(f'Sender: {user_text}')

    writer.write(user_text.encode())
    writer.write('\n'.encode())

    await writer.drain()

    raw_data_account = await reader.readline()

    account = json.loads(raw_data_account.decode())

    async with aiofiles.open('account.json', mode='a') as f:
        await f.write(json.dumps(account))

    logging.debug(f'Received: {data.decode()!r}')
    print('Вы успешно зарегистрировались')

    await submit_message(writer, reader)

asyncio.run(authorisation())
# asyncio.run(registration())
