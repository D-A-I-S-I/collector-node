import asyncio
import nats
import json
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError

async def main():
    # It is very likely that the demo server will see traffic from clients other than yours.
    # To avoid this, start your own locally and modify the example to use it.
    nc = await nats.connect("nats://daisi-broker:4222")

    # wait for data
    # put data into json format

    await nc.publish("updates", json.dumps({"id": "1", "module": "any module", "data": "nice data",}).encode())

if __name__ == "__main__":
    asyncio.run(main())