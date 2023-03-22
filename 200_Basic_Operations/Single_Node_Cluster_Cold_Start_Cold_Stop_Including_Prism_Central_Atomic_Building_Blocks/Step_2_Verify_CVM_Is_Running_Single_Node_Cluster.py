#!/usr/bin/python
"""
This script pings the CVM to see if it is running after the node has been powered on.
The cluster cannot be started until the CVM is running.
"""

# Imports
import os

# Host variables (read from file in the future)
from time import sleep

# CVM IP Address
CVM = "10.0.0.133"


def check_ping():
    # Ping the CVM with 1 ICMP packet.  A "0", indicating the CVM is active on the network.
    # This is a proxy for verifying the CVM is actually operational.  A better method would be to login to the CVM and
    # run a command like "cluster status", but we are going for simple at this point.
    hostname = CVM
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        # 0 means the CVM has responded to the ping request
        ping_status = "Network Active"
    else:
        # Any value other than 0 indicates the ping request failed
        ping_status = "Network Error"

    return ping_status


ping_result = "Starting Ping Test"

while ping_result != "Network Active":
    # Ping the CVM every 15 seconds until a successful ICMP response is received, then exit.
    ping_result = check_ping()
    sleep(15)
