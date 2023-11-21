import pyshark
from modules.common import BaseCollector
import sys
import asyncio
from asyncer import asyncify

class NetworkTrafficCollector(BaseCollector): 
    module_name = "network_traffic"

    def collect(self):
        capture =  pyshark.LiveCapture(interface='wlan0')
        for packet in capture.sniff_continuously(packet_count=1):
            self.data.append(str(packet))

    async def run(self):
        while True:
            await asyncify(self.collect)()
            await self.publish()

            # await asyncio.sleep(1)

        # async def publish(self):
        #     for point in self.data:
        #         await self.nc.publish("updates", json.dumps({"id": "1", "module": "any module", "data": point,}).encode())
