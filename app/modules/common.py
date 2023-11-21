import json
import os

import nats


class BaseCollector:
    def __init__(self, nc):
        self.nc = nc
        self.data = []

    async def send(self, module, data):
        await self.nc.publish("updates", json.dumps({"id": "1", "module": module, "data": data, }).encode())

    async def run(self):
        return
