#!/usr/bin/python
#
################################################################################
#
# This script was written by Tony Hughe for personal use.
#
# Created starting in December 2020.
#
# The script provides options for automatically starting and stopping a Nutanix
# cluster running on a private network.
#
################################################################################

#imports
import subprocess
import os

# Check if running as root or sudo
if os.geteuid() != 0:
    exit("You need to have root priveleges to run this script.\nPlease try again, this time using 'sudo'.  Exiting.")

# Host variables (read from file in the future)
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

def host_ipmi(host , user, passwd, mode):
    args = ['/usr/bin/ipmitool -H '+host+' -I lan -P '+passwd+' -U '+user+' -v power '+mode+'']
    print(args)
    subprocess.run(args, shell=True)

def start_cluster():
    print("\nStarting Cluster")
    host_ipmi(hosta, usera, passwda, "on")
    host_ipmi(hostb, userb, passwdb, "on")
    host_ipmi(hostc, userc, passwdc, "on")
    host_ipmi(hostd, userd, passwdd, "on")

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