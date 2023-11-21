import asyncio
from datetime import datetime

from modules.common import BaseCollector


class DateCollector(BaseCollector):
    async def run(self):
        while True:
            await self.send("date", {"time": datetime.now().strftime("%Y-%m-%d")})
            await asyncio.sleep(1)
