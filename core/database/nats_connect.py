from nats import connect
from nats.aio.client import Client
from nats.js import JetStreamContext


async def connect_to_nats() -> tuple[JetStreamContext]:
    nc: Client = await connect("nats://localhost:4222")
    js: JetStreamContext = nc.jetstream()

    return js