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
# if os.geteuid() != 0:
#    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'.  Exiting.")
# NOTE
# This script may need to be run more than once without root access

# Host variables (read from file in the future)
hosta = "10.0.0.131"
usera = "ADMIN"
passwda = "ADMIN"

def host_ipmi(host , user, passwd, mode):
    args = ['/usr/bin/ipmitool -H '+host+' -I lan -P '+passwd+' -U '+user+' -v power '+mode+'']
    print(args)
    subprocess.run(args, shell=True)

def stop_cluster():
    print("\Stopping Cluster")
    host_ipmi(hosta, usera, passwda, "off")

# main
stop_cluster()
