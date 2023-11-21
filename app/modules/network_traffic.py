import pyshark
from modules.common import BaseCollector
import sys
import asyncio
from asyncer import asyncify

class NetworkTrafficCollector(BaseCollector): 
    def collect(self):
        capture =  pyshark.LiveCapture(interface='wlan0')
        for packet in capture.sniff_continuously(packet_count=1):
            self.data.append(str(packet))

    async def contious_send(self):
            for point in self.data:
                print(point)
                await self.send("network_traffic", point)
                self.data.remove(point)

    async def run(self):
        while True:
            await asyncify(self.collect)()
            await self.contious_send()

            # await asyncio.sleep(1)

        # async def publish(self):
        #     for point in self.data:
        #         await self.nc.publish("updates", json.dumps({"id": "1", "module": "any module", "data": point,}).encode())
