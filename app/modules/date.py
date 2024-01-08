import asyncio
from datetime import datetime

from modules.common import BaseCollector


class DateCollector(BaseCollector):
    module_name = "date"
    async def run(self):
        while True:
            await self.send(datetime.now().strftime("%Y-%m-%d"))
            await asyncio.sleep(1)
