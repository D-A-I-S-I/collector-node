import asyncio
import json
import os
import shlex
import subprocess
import sys

import jspcap
import pyshark
from asyncer import asyncify
from modules.common import BaseCollector


class NetworkTrafficCollector(BaseCollector):
    module_name = "network_traffic"

    def __init__(self, nc):
        super().__init__(nc)
        self.interface = os.getenv("NETWORK_TRAFFIC_INTERFACE", "wlan0")
        self.packet_count = os.getenv("NETWORK_TRAFFIC_PACKET_COUNT", "1000")

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


    async def collect(self):
        command = ["tshark", "-i", self.interface, "-T", "json", "-x", "-c", str(self.packet_count)]

        # Create subprocess
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for the subprocess to finish
        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            # Process completed successfully, parse JSON output
            try:
                json_data = json.loads(stdout.decode())
                self.data.append(json_data)
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON from process output: {e}")
        else:
            # Process failed, handle errors
            print(f"Command failed with exit code {process.returncode}")
            print(f"stderr: {stderr.decode().strip()}")

    async def run(self):
        while True:
            await self.collect()
            await self.publish()
        return

    async def publish(self):
        to_remove = []
        if self.data:
            for point in self.data:
                await self.send(point)
                to_remove.append(point)

        for point in to_remove:
            self.data.remove(point)

    def collect_flow(self):
        command = "sysdig -p'%evt.num %evt.arg'" #I think it must be a number in here but did not found the field yet
        formatted_command = shlex.split(command)
        process = subprocess.Popen(formatted_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
