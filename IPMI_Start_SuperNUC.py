#!/usr/bin/python
#
################################################################################
#
# This script was written by Tony Hughes for personal use.
#
# Created starting in December 2020.
#
# The script starts SuperNUC
#
################################################################################

#imports
import subprocess
import os

# Check if running as root or sudo
# if os.geteuid() != 0:
#    exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'.  Exiting.")

# NOTE
# The script may need to be run more than once if not run with root access

# Host variables (read from file in the future)
hosta = "10.0.0.131"
usera = "ADMIN"
passwda = "ADMIN"

def host_ipmi(host , user, passwd, mode):
    args = ['/usr/bin/ipmitool -H '+host+' -I lan -P '+passwd+' -U '+user+' -v power '+mode+'']
    print(args)
    subprocess.run(args, shell=True)

def start_cluster():
    print("\nStarting Cluster")
    host_ipmi(hosta, usera, passwda, "on")

# Main
start_cluster()