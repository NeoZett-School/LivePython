import asyncio
import struct
import msgpack

class Event:
    __slots__ = ("type", "data", "conn")
    
    def __init__(self, type, data, conn=None):
        self.type = type
        self.data = data
        self.conn = conn

def encode_message(msg_type, **data):
    payload = {"type": msg_type, "data": data}
    raw = msgpack.packb(payload, use_bin_type=True)
    return struct.pack("!I", len(raw)) + raw

async def read_message(reader):
    try:
        header = await reader.readexactly(4)
    except asyncio.IncompleteReadError:
        return None

    length = struct.unpack("!I", header)[0]

    try:
        payload = await reader.readexactly(length)
    except asyncio.IncompleteReadError:
        return None

    return msgpack.unpackb(payload, raw=False)

class Connection:
    __slots__ = ("reader", "writer", "queue", "running")

    def __init__(self, reader, writer, queue):
        self.reader = reader
        self.writer = writer
        self.queue = queue
        self.running = True

    async def run(self):
        try:
            while self.running:
                msg = await read_message(self.reader)
                if msg is None:
                    break

                await self.queue.put(Event(
                    type=msg["type"],
                    data=msg["data"],
                    conn=self
                ))

        except (asyncio.IncompleteReadError, ConnectionResetError):
            pass
        finally:
            await self.queue.put(Event("disconnect", {}, self))
            await self.close()

    async def send(self, msg_type, **data):
        if not self.running:
            return

        try:
            self.writer.write(encode_message(msg_type, **data))
            await self.writer.drain()
        except ConnectionResetError:
            self.running = False

    async def close(self):
        self.running = False
        self.writer.close()
        try:
            await self.writer.wait_closed()
        except Exception:
            pass

class Server:
    __slots__ = ("server", "event_queue", "clients")

    def __init__(self):
        self.server = None
        self.event_queue = asyncio.Queue()
        self.clients = []

    async def start(self, host, port, *args, **kwargs):
        self.server = await asyncio.start_server(
            self._handle_client, 
            host=host, 
            port=port,
            *args, **kwargs
        )
        await self.server.start_serving()

    async def _handle_client(self, reader, writer):
        conn = Connection(reader, writer, self.event_queue)
        self.clients.append(conn)

        await self.event_queue.put(Event("connect", {}, conn))

        asyncio.create_task(conn.run())

    async def broadcast(self, msg_type, **data):
        for client in self.clients:
            await client.send(msg_type, **data)

    async def get_events(self):
        while True:
            try:
                yield self.event_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

    async def stop(self):
        for client in self.clients:
            await client.close()

        if self.server:
            self.server.close()
            await self.server.wait_closed()

class Client:
    __slots__ = ("reader", "writer", "conn", "event_queue")

    def __init__(self):
        self.reader = None
        self.writer = None
        self.conn = None
        self.event_queue = asyncio.Queue()

    async def connect(self, host, port, *args, **kwargs):
        self.reader, self.writer = await asyncio.open_connection(
            host=host, 
            port=port,
            *args, **kwargs
        )
        self.conn = Connection(self.reader, self.writer, self.event_queue)

        asyncio.create_task(self.conn.run())

    async def send(self, msg_type, **data):
        if self.conn:
            await self.conn.send(msg_type, **data)

    async def get_events(self):
        while True:
            try:
                yield self.event_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

    async def disconnect(self):
        if self.conn:
            await self.conn.close()