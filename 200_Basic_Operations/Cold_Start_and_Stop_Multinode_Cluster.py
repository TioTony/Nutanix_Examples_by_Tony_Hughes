#!/usr/bin/python
#
################################################################################
# TH December 2022
#
# This script will prompt to power-on or power-off a multi-node cluster.
#
# It will not start or stop any additional VMs.
#
# Any other VMs must be manually started and stopped.
#
# This script requires the linux "ipmitool" and root access, although
# it will sometimes work without root. My use of it was inconsistent so
# I just included running as root as the default.
#
# This script is fully self-contained and does not rely on any other files.
#
################################################################################

#imports
import subprocess
import os
from time import sleep

import paramiko


# Class to capture the details of each node
# - impihostip is the IP address for the IPMI interface
# - ipmiuser is the username for the IPMI interface
# - ipmipass is the password for the IPMI interface
# - cvmip is the ip address for the CVM running on the node
# - cvmuser is the CVM user for the CVM running on the node
# - cvmpass is the password for the CVM user above
class NTNXNode:
   def __init__(self, ipmihostip, ipmiuser, ipmipass, cvmip, cvmuser, cvmpass):
       self.ipmihostip = ipmihostip
       self.ipmiuser = ipmiuser
       self.ipmipass = ipmipass
       self.cvmip = cvmip
       self.cvmuser = cvmuser
       self.cvmpass = cvmpass

# Class to capture the details of the cluster
# - clustervip is the Cluster Virtual IP
# - clusterport is the port to access Prism on the Cluster VIP
# - clusteruser is the user used to access Prism
# - clsuterpass is the password for the Prism users above
class NTNXCluster:
    def __init__(self, clustervip, clusterport, clusteruser, clusterpass):
        self.clustervip = clustervip
        self.clusterport = clusterport
        self.clusteruser = clusteruser
        self.clusterpass = clusterpass

#Define each node here
nodea = NTNXNode("10.0.0.101", "ADMIN", "ADMIN", "10.0.0.109", "nutanix", "nutanix/4u")
nodeb = NTNXNode("10.0.0.102", "ADMIN", "ADMIN", "10.0.0.110", "nutanix", "nutanix/4u")
nodec = NTNXNode("10.0.0.103", "ADMIN", "ADMIN", "10.0.0.111", "nutanix", "nutanix/4u")
noded = NTNXNode("10.0.0.104", "ADMIN", "ADMIN", "10.0.0.112", "nutanix", "nutanix/4u")

#Put all the nodes in a tuple
nodetuple = (nodea, nodeb, nodec, noded)

#Define the clusters
cluster1 = NTNXCluster("10.0.0.113", "9440", "admin", "nx2Tech714!")

# command use to start the cluster
clusterstartcommand = "/usr/local/nutanix/cluster/bin/cluster start"


# Ping the CVMs to ensure they are available before starting the cluster
# Any CVM that does not return a ping packet will set the status to "Network Error"
# If all CVMs return the ping successfully the status will be "Network Active"
def check_ping():
    ping_status = "Network Active"
    for node in nodetuple:
       response = os.system("ping -c 1 " + node.cvmip)
       # and then check the response...
       if response == 0:
           # do nothing
           print('\nPing successful: ' + node.cvmip)
       else:
           # Any value other than 0 indicates the ping request failed
           print('\nPing failed: ' + node.cvmip)
           ping_status = "Network Error"
    return ping_status

# Take the passed input variables and boot the node
def host_ipmi(host , user, passwd, mode):
    args = ['/usr/bin/ipmitool -H '+host+' -I lan -P '+passwd+' -U '+user+' -v power '+mode+'']
    print(args)
    subprocess.run(args, shell=True)

def cluster_cli_start():
    # Establish an SSH session with paramiko
    ssh = paramiko.SSHClient()
    # Accept ssh key if this is the first time connecting.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Create an ssh connection to the First CVM in the tuple
    ssh.connect(nodetuple[0].cvmip, username=nodetuple[0].cvmuser, password=nodetuple[0].cvmpass)
    # Execute the command to start the cluster.  Capture stdin, stdout, and stderr from the command.
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(clusterstartcommand)
    # Print stdout from the command
    print(ssh_stdout.read().decode())
    # Print stderr from the command
    print(ssh_stderr.read().decode())
    # Cleanly close the ssh session
    ssh.close()
def start_cluster():
    print("\nStarting Cluster")
    for node in nodetuple:
        host_ipmi(node.ipmihostip, node.ipmiuser, node.ipmipass, "on")
    # Ping the CVM until it responds
    ping_result = "Starting Ping Test"
    while ping_result != "Network Active":
        # Ping the CVMs every 15 seconds until a successful ICMP response is received from all CVMs, then exit.
        ping_result = check_ping()
        sleep(15)
    # Wait 60 seconds once CVM is responsive to ensure it is accepting requests
    sleep(60)
    # Start the cluster
    cluster_cli_start()
    # NEED TO UPDATE
    # sleep(600)
    # start_prism_central()



# Main Menu
menu = {}
menu['1']="Start Cluster"
# menu['2']="Stop Cluster"
menu['q']="Exit"
while True:
    options=menu.keys()
    for entry in options:
        print(entry, menu[entry])

    selection=input("Please Select:")
    if selection =='1':
        start_cluster()
    # elif selection =='2':
    #    stop_cluster()
    elif selection =='q':
        break
    else:
        print("\n Invalid Selection")