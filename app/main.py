import asyncio
import nats
import json
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError
import pyshark
import os
from asyncer import asyncify

#3. does not work either
def capture2():
    arr = []
    capture =  pyshark.LiveCapture(interface='wlo1')
    for packet in capture.sniff_continuously(packet_count=5):
        arr.append(str(packet))
    return arr

async def main():
    # It is very likely that the demo server will see traffic from clients other than yours.
    # To avoid this, start your own locally and modify the example to use it.
    nats_url = os.getenv("BROKER_URL", "nats://localhost:4222")
    nc = await nats.connect(nats_url)
    arr = await asyncify(capture2)()
    for i in arr:
        await nc.publish("updates", json.dumps({"id": "1", "module": "any module", "data": i,}).encode())


if __name__ == "__main__":
    asyncio.run(main())