import asyncio
import nats
import os
import json
from nats.errors import ConnectionClosedError, TimeoutError, NoServersError

class Collector:
    @classmethod
    async def create(cls):
        self = cls()
        self.modules = []
        self.nats_url = os.getenv("BROKER_URL", "nats://localhost:4222")
        self.nc = await nats.connect(self.nats_url)
        return self

    async def send(self):
        await self.nc.publish("updates", json.dumps({"id": "1", "module": "any module", "data": "nice data",}).encode())


async def main():
    collector = await Collector.create()
    await collector.send()

if __name__ == "__main__":
    asyncio.run(main())
