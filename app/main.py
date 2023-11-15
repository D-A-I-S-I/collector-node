import asyncio
import nats
import os
import json
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError

async def main():
    nats_url = os.getenv("BROKER_URL", "nats://localhost:4222")
    nc = await nats.connect(nats_url)

    # wait for data
    # put data into json format

    await nc.publish("updates", json.dumps({"id": "1", "module": "any module", "data": "nice data",}).encode())

if __name__ == "__main__":
    asyncio.run(main())
