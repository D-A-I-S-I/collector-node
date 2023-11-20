import pyshark
from modules.common import BaseCollector
import sys

class NetworkTrafficCollector(BaseCollector): 

    def __init__(self):
        super().__init__()

    def collect(self):
        capture =  pyshark.LiveCapture(interface='wlo1')
        for packet in capture.sniff_continuously(packet_count=5):
            self.data.append(str(packet))
    
    async def publish(self):
        await super().publish()
        return