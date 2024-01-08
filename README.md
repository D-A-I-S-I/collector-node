# Collector Node

This repository contains the code for the collector node. 

> Note: Start the broker (automatic using make) from the Compute node before running the Collector node.

## Installation

Clone the repository:

```sh
git clone https://github.com/D-A-I-S-I/collector-node.git
cd collector-node
```

## Environment Variables

To set the PID of the process you want to collect syscalls from:

```sh
export SYSTEM_CALLS_PIDS=<desired-pid>
```

To select which modules to collect data for:

```sh
export ENABLED_MODULES=network_traffic,system_calls
```

To select which interface to collect network packets from (*wlan0* or *eth0* for example):

```sh
export NETWORK_TRAFFIC_INTERFACE=<desired-interface>
```

## Running

To run the collector node locally, use the following command (this creates and activates a virtual environment as well):

```python
sudo -E make
```

(There are commands for running with Docker, but it is not currently working with torch in this setup.)


### Cleaning Up
To clean up the environment, use the following command:

```python
sudo make clean
```
