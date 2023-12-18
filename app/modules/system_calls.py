import asyncio
import json
import os
import shlex
import subprocess
import sys
from queue import Empty, Queue
from threading import Thread

from modules.common import BaseCollector


class SystemCallsCollector(BaseCollector):
    module_name = "system_calls"
    pids = os.getenv("SYSTEM_CALLS_PIDS")

    async def run(self):
        self.data = ""
        if len(self.pids.split(",")) == 1:
            self.strace_column_with_digits = 1
        else:
            self.strace_column_with_digits = 3
        await asyncio.gather(self.publish(), self.collect())
        return

    async def publish(self):
        while True:
            if self.data:
                await self.send(self.data)
                self.data = ""
            await asyncio.sleep(1)

    async def collect(self):
        def enqueue_output(out, queue):
            for line in iter(out.readline, b''):
                queue.put(line)
            out.close()

        command = ["strace", "-n", "--silent=all", "-p", self.pids]
        p = subprocess.Popen(command, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True, bufsize=1)
        q = Queue()
        t = Thread(target=enqueue_output, args=(p.stderr, q))
        t.daemon = True
        t.start()

        while True:
            if p.poll() is not None:  # Check if subprocess has terminated
                error_message = p.stderr.read()
                print(f"strace failed to run: {error_message}")
                break  # Exit the loop or perform other error handling
            try:
                line = q.get_nowait()
                digits = line.split()[
                    self.strace_column_with_digits].strip("]")
                self.data = self.data + " " + digits
            except Empty:
                pass
            await asyncio.sleep(0.1)
