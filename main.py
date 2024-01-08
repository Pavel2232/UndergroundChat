import asyncio


async def tcp_client():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5000)

    while True:
        data = await reader.read(1000)
        print(f'Received: {data.decode()}')


asyncio.run(tcp_client())
