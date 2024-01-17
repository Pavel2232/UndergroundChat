import asyncio
import datetime
import time

import aiofiles

import gui
from socket_context_manager import Socket


async def save_messages(message, queue):
    async with aiofiles.open('boss.txt', mode='a') as f:
        await queue.put(await f.write(message))


async def generate_msgs(queue):
    for _ in range(100):
        await queue.put(f'''ping {time.time()}''')
        await asyncio.sleep(1)
    return None

# async def read_msgs(host, port, queue):
async def read_msgs(queue, queue_write):

    socket = Socket('minechat.dvmn.org', 5000)

    while True:
        async with socket:
            data_chanel = await socket.reader.readline()
            date = f'[{datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}] '
            message = data_chanel.decode()
            log_message = date + message
            await save_messages(log_message, queue_write)
            await queue.put(message)





async def main():
    messages_queue = asyncio.Queue()
    # messages_queue.put_nowait('''Привет обитателям чата!
    # Как дела?''')
    write_file_queue = asyncio.Queue()
    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        async with aiofiles.open('boss.txt', mode='r') as f:
            messages_queue.put_nowait(await f.read())
        tg.create_task(read_msgs(messages_queue, write_file_queue))


        return await gui.draw(messages_queue, sending_queue, status_updates_queue)



if __name__ == '__main__':

    # messages_queue = asyncio.Queue()
    # # messages_queue.put_nowait('''Привет обитателям чата!
    # # Как дела?''')
    #
    # sending_queue = asyncio.Queue()
    # status_updates_queue = asyncio.Queue()

    asyncio.run(main())