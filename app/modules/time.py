import asyncio
from datetime import datetime

from modules.common import BaseCollector


class TimeCollector(BaseCollector):
    async def run(self):
        while True:
            await self.send("time", {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            await asyncio.sleep(1)
