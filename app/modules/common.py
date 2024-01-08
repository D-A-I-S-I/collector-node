import json
import os
import pickle

import nats


class BaseCollector:
    module_name = "base"

    def __init__(self, nc):
        self.nc = nc
        self.data = []

    async def send(self, data):
        await self.nc.publish("updates", pickle.dumps(data), headers={'module_name': self.module_name})

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
