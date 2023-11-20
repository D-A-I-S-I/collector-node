import pyshark
import BaseCollector

class NetworkTrafficCollector(BaseCollector): 

    def __init__(self):
        super().__init__(self)

    def collect():
        arr = []
        capture =  pyshark.LiveCapture(interface='wlo1')
        for packet in capture.sniff_continuously(packet_count=5):
            arr.append(str(packet))
    
    def publish():
        return