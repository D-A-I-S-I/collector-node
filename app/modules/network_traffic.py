import json
import pyshark
import jspcap
import subprocess
import os
from modules.common import BaseCollector
import sys
import asyncio
from asyncer import asyncify
import shlex


class NetworkTrafficCollector(BaseCollector): 
    module_name = "network_traffic"

    def print_callback(pkt):
        print("ho")
        return
        print(type(pkt))
        #self.data.append(pkt)

    def transform(self,inputfile):
        #command = "../FlowMeter/pkg/flowmeter -ifLiveCapture=false -fname=packet -maxNumPackets=40000000 -ifLocalIPKnown false INFO[0000] Liv" 
        #command = "tshark -r packet.pcap -T json -x > packet.json"
        #formatted_command = shlex.split(command)
        #subprocess.run(formatted_command)
        with open("outfile.json","w") as outfile:
            subprocess.run(["tshark", "-r",
                os.path.join(inputfile),
                "-T", "json", "-x"],
                stdout=outfile, check=True)
               
    
    def collect(self):
        file = "packet.pcap"
        output = open(file, "w")
        print(type(output))
        capture = pyshark.LiveCapture(interface="wlo1", output_file=file)
        capture.sniff(packet_count=15000)
        output.close()
        self.transform(file)

        with open("outfile.json", 'r') as openfile:
            json_object = json.load(openfile)
        self.data.append(json_object)
        return

    async def run(self):
        while True:
            await asyncify(self.collect)()
            await self.publish()

    async def publish(self):
        # for point in self.data:
        await self.nc.publish("updates", json.dumps({"id": "1", "module": "network_traffic", "data": self.data,}).encode())

    def collect_flow(self):
        command = "sysdig -p'%evt.num %evt.arg'" #I think it must be a number in here but did not found the field yet
        formatted_command = shlex.split(command)
        process = subprocess.Popen(formatted_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
