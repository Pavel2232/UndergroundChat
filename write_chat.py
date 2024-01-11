import argparse
import asyncio
import json
import logging

import aiofiles

from socket_context_manager import Socket

logging.getLogger(__name__)
logging.basicConfig(
    level=1
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



async def authorisation(token, host, port):
    socket = Socket(host, port)

    async with socket:
        socket.writer.write(f'{token}'.encode())
        await socket.writer.drain()

        socket.writer.write('\n'.encode())
        await socket.writer.drain()

        await socket.reader.read(1000)
        recived = await socket.reader.read(1000)
        print(recived.decode())

        if recived.decode().startswith('\nnull'):
            print(
                'Неизвестный токен. Проверьте его или зарегистрируйте заново.'
            )

        else:
            await submit_message(socket.writer, socket.reader)


async def registration(user_name: str, host, port):
    socket = Socket(host, port)

    async with socket:
        socket.writer.write('\n'.encode())
        await socket.writer.drain()

        data = await socket.reader.read(1000)
        print(f'data: {data.decode()}')

        user_text = user_name.rstrip()
        logging.debug(f'Sender: {user_text}')

        socket.writer.write(user_text.encode())
        socket.writer.write('\n'.encode())

        await socket.writer.drain()

        raw_data_account = await socket.reader.readline()

        account = json.loads(raw_data_account.decode())

        async with aiofiles.open('account.json', mode='a') as f:
            await f.write(json.dumps(account))

        logging.debug(f'Received: {data.decode()!r}')
        print('Вы успешно зарегистрировались')


        await submit_message(socket.writer, socket.reader)

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
        default=5050
    )

    parser.add_argument(
        "-t",
        "--token",
        help="Токен пользователя",
        type=str,
    )
    args = parser.parse_args()

    if args.token:
        asyncio.run(authorisation(args.token, host=args.host, port=args.port))

    if args.username:
        asyncio.run(registration(args.token, host=args.host, port=args.port))


