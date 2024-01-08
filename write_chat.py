import asyncio


async def tcp_echo_client():
    reader, writer = await asyncio.open_connection(
        'minechat.dvmn.org', 5050)

    writer.write('1d1405f0-ae49-11ee-aae7-0242ac110002'.encode())
    await writer.drain()

    writer.write('\n'.encode())
    await writer.drain()

    while True:
        ok = input()

        writer.write(ok.encode())
        await writer.drain()

        writer.write('\n'.encode())
        await writer.drain()

        writer.write('\n'.encode())
        await writer.drain()

        data = await reader.read(1000)
        print(f'Received: {data.decode()!r}')


asyncio.run(tcp_echo_client())
