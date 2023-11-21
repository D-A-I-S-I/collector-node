import asyncio
import json
import logging
import os
from dataclasses import dataclass

import modules
import nats
from nats.errors import ConnectionClosedError, NoServersError, TimeoutError


class Collector:
    @classmethod
    async def create(cls):
        self = cls()
        self.enabled_modules = os.getenv(
            "ENABLED_MODULES", "network_traffic").split(",")
        self.tasklist = []
        self.nats_url = os.getenv("BROKER_URL", "nats://localhost:4222")
        self.nc = await nats.connect(self.nats_url)
        print(f"Connected to {self.nats_url}")
        print(f"Enabled modules: {self.enabled_modules}")
        return self

    async def run(self):
        print("Running")
        for module in self.enabled_modules:
            if module == 'network_traffic':
                print("Network traffic module")
                self.tasklist.append(modules.NetworkTrafficCollector(self.nc))
            elif module == 'time':
                print("Time module")
                self.tasklist.append(modules.TimeCollector(self.nc))
            elif module == 'date':
                print("Date module")
                self.tasklist.append(modules.DateCollector(self.nc))
            else:
                print(f"Module {module} not found")

        await asyncio.gather(*[task.run() for task in self.tasklist])
        await self.nc.drain()
        return


async def main():
    collector = await Collector.create()
    await collector.run()
    print("Done")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
