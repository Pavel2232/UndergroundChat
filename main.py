import asyncio
import time

import gui
from socket_context_manager import Socket


async def generate_msgs(queue):
    for _ in range(100):
        await queue.put(f'''ping {time.time()}''')
        await asyncio.sleep(1)
    return None

# async def read_msgs(host, port, queue):
async def read_msgs(queue):

    socket = Socket('minechat.dvmn.org', 5000)

    while True:
        async with socket:
            data_chanel = await socket.reader.readline()
            # date = f'[{datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")}] '
            log_message = data_chanel.decode()
            # await write_message_file(log_message, history_file=history_file)
            await queue.put(log_message)





async def main():
    messages_queue = asyncio.Queue()
    # messages_queue.put_nowait('''Привет обитателям чата!
    # Как дела?''')

    sending_queue = asyncio.Queue()
    status_updates_queue = asyncio.Queue()
    async with asyncio.TaskGroup() as tg:
        tg.create_task(read_msgs(messages_queue))

        return await gui.draw(messages_queue, sending_queue, status_updates_queue)



if __name__ == '__main__':

    # messages_queue = asyncio.Queue()
    # # messages_queue.put_nowait('''Привет обитателям чата!
    # # Как дела?''')
    #
    # sending_queue = asyncio.Queue()
    # status_updates_queue = asyncio.Queue()

    asyncio.run(main())