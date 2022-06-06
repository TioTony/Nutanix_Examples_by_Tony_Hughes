#!/usr/bin/python
"""
This script changed the IPMI power state of a single node to "off".
It is intended to be used as a simplified example of using the Nutanix node's IPMI interface
This script has no guard rails.  Make sure you have shut down the VMs, PC, cluster, and CVM
before running this script or you may have problems.
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
    # Accept the IPMI IP address, username, password, and powerstate.  Use this info to power off the node.
    args = ['/usr/bin/ipmitool -H '+host+' -I lan -P '+passwd+' -U '+user+' -v power '+mode+'']
    print(args)
    subprocess.run(args, shell=True)

def stop_cluster():
    # Pass the IPMI IP address, username, password and powerstate to the host_ipmi function
    print("\Stopping Cluster")
    host_ipmi(hosta, usera, passwda, "off")

# main
stop_cluster()
