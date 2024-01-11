import asyncio



class Socket:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.writer: asyncio.StreamWriter = None
        self.reader: asyncio.StreamReader = None

    async def __aenter__(self):
        reader, writer = await asyncio.open_connection(
            self.host, self.port)
        self.reader = reader
        self.writer = writer

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.writer.close()
        await self.writer.wait_closed()
