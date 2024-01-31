import asyncio
import datetime
import json
import logging
from tkinter import messagebox
import aiofiles
import gui
from socket_context_manager import Socket
from async_timeout import timeout

logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
    level='INFO'
)


# async def send_msgs(host, port, queue):
async def send_msgs(queue, message_queue, status_queue, nickname: str, watchdog_queue):
    # socket = Socket('minechat.dvmn.org', 5050)

    status_queue.put_nowait(gui.SendingConnectionStateChanged.ESTABLISHED)
    while True:
        sms = await queue.get()
        await generate_msgs(message_queue, sms, nickname, watchdog_queue)
    status_queue.put_nowait(gui.SendingConnectionStateChanged.CLOSED)


async def save_messages(message, queue):
    async with aiofiles.open('boss.txt', mode='a') as f:
        await queue.put(await f.write(message))


async def generate_msgs(queue, sms, nickname: str, read_watch):
    await queue.put(f'{nickname}: {sms}\n')
    read_watch.put_nowait('Send')


# async def read_msgs(host, port, queue):
async def read_msgs(queue, queue_write, status_queue, read_watch):
    socket = Socket('minechat.dvmn.org', 5000)
    status_queue.put_nowait(gui.ReadConnectionStateChanged.ESTABLISHED)
    while True:
            async with socket:
                try:
                    async with timeout(4) as cm:
                        data_chanel = await socket.reader.readline()
                        date = f'[{datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}] '
                        message = data_chanel.decode()
                        log_message = date + message

                        await save_messages(log_message, queue_write)
                        await queue.put(message)
                        read_watch.put_nowait('New message')
                except TimeoutError:
                    read_watch.put_nowait(cm.deadline)
                    status_queue.put_nowait(gui.ReadConnectionStateChanged.CLOSED)


async def watch_for_connection(queue):
    while True:
        sms = await queue.get()
        logging.info(sms)


async def main():
    messages_queue = asyncio.Queue()

    write_file_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    watchdog_queue = asyncio.Queue()

    socket = Socket('minechat.dvmn.org', 5050)

    async with asyncio.TaskGroup() as tg:
        async with aiofiles.open('boss.txt', mode='r') as f:
            messages_queue.put_nowait(await f.read())

        async with socket:
            socket.writer.write('5efd0c92-b0be-11ee-aae7-0242ac110002\n\n'.encode())
            await socket.writer.drain()

            await socket.reader.read(1000)
            recived = await socket.reader.readline()

            recived_json = json.loads(recived)

            if not recived_json:
                messagebox.showinfo('ok', gui.InvalidToken())

        messages_queue.put_nowait(f'''Выполнена авторизация. Пользователь {recived_json.get('nickname')}\n''')
        event = gui.NicknameReceived(recived_json.get('nickname'))
        status_updates_queue.put_nowait(event)
        status_updates_queue.put_nowait(gui.ReadConnectionStateChanged.INITIATED)  # устанавливаем соединение
        status_updates_queue.put_nowait(gui.SendingConnectionStateChanged.INITIATED)

        tg.create_task(watch_for_connection(watchdog_queue))

        tg.create_task(
            read_msgs(
                messages_queue,
                write_file_queue,
                status_updates_queue,
                watchdog_queue
            )

        )
        tg.create_task(
            send_msgs(
                sending_queue,
                messages_queue,
                status_updates_queue,
                recived_json.get('nickname'),
                watchdog_queue

            )
        )

        tg.create_task(gui.draw(messages_queue, sending_queue, status_updates_queue))


if __name__ == '__main__':

    asyncio.run(main())
