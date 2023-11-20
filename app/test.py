from modules import NetworkTrafficCollector
import asyncio
from asyncer import asyncify

#simple test if network_traffic class is working
async def test_networking_class():
    nw_collector = await NetworkTrafficCollector.create()
    await asyncify(nw_collector.collect)()
    await nw_collector.publish()

asyncio.run(test_networking_class())
