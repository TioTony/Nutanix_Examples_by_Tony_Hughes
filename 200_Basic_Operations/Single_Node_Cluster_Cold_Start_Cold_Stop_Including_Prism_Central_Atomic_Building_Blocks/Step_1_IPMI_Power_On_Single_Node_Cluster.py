#!/usr/bin/python
#
"""
This script changed the IPMI power state of a single node to "on".
It is intended to be used as a simplified example of using the Nutanix node's IPMI interface
"""

#imports
import subprocess
import os

# Host variables
# Node IPMI IP Address
hosta = "10.0.0.131"
# Node IPMI Username
usera = "ADMIN"
# Node IPMI Password
passwda = "ADMIN"

def host_ipmi(host , user, passwd, mode):
    # Accept the IPMI IP address, username, password, and powerstate.  Use this info to power on the node.
    args = ['/usr/bin/ipmitool -H '+host+' -I lan -P '+passwd+' -U '+user+' -v power '+mode+'']
    print(args)
    subprocess.run(args, shell=True)

def start_cluster():
    # Pass the IPMI IP address, username, password and powerstate to the host_ipmi function
    print("\nStarting Cluster")
    host_ipmi(hosta, usera, passwda, "on")

# Main
start_cluster()