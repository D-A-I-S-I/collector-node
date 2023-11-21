from modules import NetworkTrafficCollector, SystemCallsCollector
import asyncio
from asyncer import asyncify

#simple test if network_traffic class is working
async def test_networking_class():
    nw_collector = await NetworkTrafficCollector.create()
    await asyncify(nw_collector.collect)()
    await nw_collector.publish()

async def test_system_calls_class():
    nw_collector = await SystemCallsCollector.create()
    await asyncify(nw_collector.collect)()
    await nw_collector.publish()

asyncio.run(test_system_calls_class())
