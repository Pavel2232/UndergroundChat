import argparse
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


async def authorisation(token):
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    writer.write(f'{token}'.encode())
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

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-u",
        "--username",
        help="Имя пользователя, программа запусит регистрацию",
    )

    parser.add_argument(
        "-host",
        "--host",
        help="Хост",
        default='minechat.dvmn.org'
    )

    parser.add_argument(
        "-p",
        "--port",
        help="Порт",
        type=int,
        default=5000
    )

    parser.add_argument(
        "-t",
        "--token",
        help="Токен пользователя",
        type=str,
    )
    args = parser.parse_args()

    if args.token:
        asyncio.run(authorisation(args.token))

    if args.username:
        asyncio.run(registration())


