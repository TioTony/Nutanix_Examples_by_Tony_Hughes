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
import json

# Opening JSON file
f = open('test.json')

#returns JSON object as a dictionary
data = json.load(f)

# Iterate through and print json contents
for i in data['cluster_details']:
    #print(i)
    # print(i["cluster_name"])
    clusterName = i["cluster_name"]
    hostA = i["hosta"]
    userA = i["usera"]
    passwdA = i["passwda"]
    print(clusterName)
    print(hostA)
    print(userA)
    print(passwdA)

# Close file
f.close()
