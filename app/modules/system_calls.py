import subprocess
from modules.common import BaseCollector
import sys
import json

class SystemCallsCollector(BaseCollector): 
    module_name = "system_calls"

    async def collect(self):
        command = ['strace', '-f',"ls" ,"-l"] #switch to other comment later
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Check for errors
        if process.returncode != 0:
            print(f"Error running strace: {stderr.decode('utf-8')}")
            return None

        # Parse the strace output and extract system calls
        strace_output = stdout.decode('utf-8')
        system_calls = [line.strip() for line in strace_output.split('\n') if line.strip()]

        # Convert system calls to JSON
        json_data = json.dumps(system_calls, indent=2)

        self.data.append(json_data)
