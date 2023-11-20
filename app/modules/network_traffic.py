import pyshark
from modules import BaseCollector

class NetworkTrafficCollector(BaseCollector): 

    def __init__(self):
        super().__init__(self)

    def collect(self):
        capture =  pyshark.LiveCapture(interface='wlo1')
        for packet in capture.sniff_continuously(packet_count=5):
            self.data.append(str(packet))
    
    async def publish():
        super.publish()
        return