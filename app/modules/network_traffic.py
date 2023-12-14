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
        #tshark -r input.pcap -T json >output.json
        with open("outfile.json","w") as outfile:
            subprocess.run(["tshark", "-r",
                os.path.join(inputfile),
                "-T", "json"],
                stdout=outfile, check=True)
    
    def collect(self):
        file = "packet.pcap"
        output = open(file, "w")
        print(type(output))
        capture = pyshark.LiveCapture(interface="wlo1", output_file=file)
        capture.sniff(10)
        output.close()
        json_file = self.transform(file)
        print(type(json_file))
        with open("outfile.json", 'r') as openfile:
            json_object = json.load(openfile)
        self.file = json_object
        return

    async def run(self):
        while True:
            await asyncify(self.collect)()
            await self.publish()


    async def publish(self):
        # for point in self.data:
        await self.nc.publish("updates", json.dumps({"id": "1", "module": "any module", "data": self.file,}).encode())

    def collect_flow(self):
        command = "sysdig -p'%evt.num %evt.arg'" #I think it must be a number in here but did not found the field yet
        formatted_command = shlex.split(command)
        process = subprocess.Popen(formatted_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
