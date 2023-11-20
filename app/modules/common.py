import nats
import os
import json
class BaseCollector:
    def __init__(self):
        return

    @classmethod
    async def create(cls):
        self = cls()
        self.data = []
        self.nats_url = os.getenv("BROKER_URL", "nats://localhost:4222")
        self.nc = await nats.connect(self.nats_url)
        return self

    def collect(self):
        return

    async def publish(self):
        for point in self.data:
            await self.nc.publish("updates", json.dumps({"id": "1", "module": "any module", "data": point,}).encode())
        return
