import json
import os

import nats


class BaseCollector:
    module_name = "base"

    def __init__(self, nc):
        self.nc = nc
        self.data = []

    async def send(self, data):
        await self.nc.publish("updates", json.dumps({"id": "1", "module": self.module_name, "data": data, }).encode())

    async def publish(self):
        for point in self.data:
            await self.send(point)
            self.data.remove(point)

    async def collect(self):
        pass

    async def run(self):
        while True:
            await self.collect()
            await self.publish()
        return
