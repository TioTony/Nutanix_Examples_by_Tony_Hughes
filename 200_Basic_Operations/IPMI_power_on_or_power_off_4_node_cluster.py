#!/usr/bin/python
#
################################################################################
#
# This script will prompt to power-on or power-off a 4 Node cluster.
#
# It will not start or stop any additional VMs including Prism Central.
#
# It will not perform a "cluster stop", shutdown CVMs, or put nodes into
# a maintenance mode.  Those steps must be done manually.
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

# Check if running as root or sudo
#if os.geteuid() != 0:
#    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'.  Exiting.")

# Host variables
# host<n> is the IPMI IP address
# user<n> is the IPMI user
# passwd<n> is the IPMI password
# Update these to match the existing 4 node cluster
hosta = "10.0.0.101"
usera = "ADMIN"
passwda = "ADMIN"
hostb = "10.0.0.102"
userb = "ADMIN"
passwdb = "ADMIN"
hostc = "10.0.0.103"
userc = "ADMIN"
passwdc = "ADMIN"
hostd = "10.0.0.104"
userd = "ADMIN"
passwdd = "ADMIN"

# Take the passed input variables and boot the node
def host_ipmi(host , user, passwd, mode):
    args = ['/usr/bin/ipmitool -H '+host+' -I lan -P '+passwd+' -U '+user+' -v power '+mode+'']
    print(args)
    subprocess.run(args, shell=True)

# Run the above host_ipmi command to change the power state for each node to "on"
def start_cluster():
    print("\nStarting Cluster")
    host_ipmi(hosta, usera, passwda, "on")
    host_ipmi(hostb, userb, passwdb, "on")
    host_ipmi(hostc, userc, passwdc, "on")
    host_ipmi(hostd, userd, passwdd, "on")

# Run the above host_ipmi command to change the power state for each node to "off"
def stop_cluster():
    print("\Stopping Cluster")
    host_ipmi(hosta, usera, passwda, "off")
    host_ipmi(hostb, userb, passwdb, "off")
    host_ipmi(hostc, userc, passwdc, "off")
    host_ipmi(hostd, userd, passwdd, "off")

# Main Menu
menu = {}
menu['1']="Start Cluster"
menu['2']="Stop Cluster"
menu['q']="Exit"
while True:
    options=menu.keys()
    for entry in options:
        print(entry, menu[entry])

    selection=input("Please Select:")
    if selection =='1':
        start_cluster()
    elif selection =='2':
        stop_cluster()
    elif selection =='q':
        break
    else:
        print("\n Invalid Selection")