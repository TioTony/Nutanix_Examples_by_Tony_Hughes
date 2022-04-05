#!/usr/bin/python
#
################################################################################
#
# This script was written by Tony Hughes for personal use.
#
# Created 4/5/2022
#
# This script does a "ping" to verify the CVM is running
#
################################################################################

# Imports
import os

# Host variables (read from file in the future)
from time import sleep

CVM = "10.0.0.133"


def check_ping():
    hostname = CVM
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        ping_status = "Network Active"
    else:
        ping_status = "Network Error"

    return ping_status


ping_result = check_ping()
print(ping_result)

while ping_result != "Network Active":
    ping_result = check_ping()
    sleep(15)
