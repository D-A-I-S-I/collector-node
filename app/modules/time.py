import asyncio
from datetime import datetime

from modules.common import BaseCollector


class TimeCollector(BaseCollector):
    module_name = "time"
    async def run(self):
        while True:
            await self.send({"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            await asyncio.sleep(1)
