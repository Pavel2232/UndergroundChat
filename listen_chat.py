import argparse
import asyncio
import datetime
import aiofiles

from socket_context_manager import Socket


async def write_message_file(message, history_file):
    async with aiofiles.open(f'{history_file}', mode='a') as f:
        await f.write(message)


async def tcp_client(host: str, port: int, history_file: str):
    socket = Socket(host, port)

    while True:
        async with socket:
            data_chanel = await socket.reader.readline()
            date = f'[{datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}] '
            log_message = date + data_chanel.decode()
            await write_message_file(log_message, history_file=history_file)
            print(f'{log_message}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
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
        "-path",
        "--path",
        help="Путь к файлу с историей переписки",
        type=str,
        default='chat.txt'
    )
    args = parser.parse_args()

    if args.host and args.port and args.path:
        host = args.host
        port = args.port
        history_file = args.path

    asyncio.run(tcp_client(
        host=args.host,
        port=args.port,
        history_file=args.path
    )
    )


