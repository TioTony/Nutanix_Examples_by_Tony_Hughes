#!/usr/bin/python
"""
This script can fully start or fully stop a single node cluster with a
single PCVM

The "Start" portion will start the node from a cold state using IPMITool.
It will start the cluster and boot Prism Central.

The "Stop" portion will shutdown any running VMs or alert if it cannot.
It will shutdown Prism Central, Stop the cluster, shutdown the CVM, and
use IPMITool to poweroff the physical node.

TBD:
- Add code to stop all running VMs
- Add code to verify PC and other VMs are all stopped
- Clean up/consolidate some of the variables and code
- Clean up formatting

"""

# imports

import subprocess
import os
import sys
from time import sleep
import paramiko
import requests
import urllib3
import json

# Host variables
# Node IPMI IP Address
from requests.auth import HTTPBasicAuth

hosta = "10.0.0.131"
# Node IPMI Username
usera = "ADMIN"
# Node IPMI Password
passwda = "ADMIN"
# CVM IP Address
CVM = "10.0.0.133"
# CVM linux shell username for ssh
user = "nutanix"
# CVM user password.  The example below is the default password for Nutanix installations.
passwd = "nutanix/4u"
# command use to start the cluster
command = "/usr/local/nutanix/cluster/bin/cluster start"
# IP Address for a CVM or the Prism Element Cluster VIP
CLUSTER_IP = "10.0.0.133"
# Cluster port
CLUSTER_PORT = "9440"
# Prism Element Local Admin account
CLUSTER_USERNAME = "admin"
# Prism Element Admin Password.  I realise this is my password, but it is on a segmented network in my home lab.
CLUSTER_PASSWORD = "nx2Tech1242!"

def host_ipmi(host , user, passwd, mode):
    # Accept the IPMI IP address, username, password, and powerstate.  Use this info to power on the node.
    args = ['/usr/bin/ipmitool -H '+host+' -I lan -P '+passwd+' -U '+user+' -v power '+mode+'']
    print(args)
    subprocess.run(args, shell=True)

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

def shutdown_cvm():
    # Command used to stop the CVM
    command = "sudo shutdown -P now"
    # Establish an SSH session with paramiko
    ssh = paramiko.SSHClient()
    # Accept ssh key if this is the first time connecting.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Create an ssh connection to the CVM using the user and password supplied above
    ssh.connect(CVM, username=user, password=passwd)
    # Execute the command to stop the CVM.  Capture stdin, stdout, and stderr from the command.
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    # Print stdout from the command
    print(ssh_stdout.read().decode())
    # Print stderr from the command
    print(ssh_stderr.read().decode())
    # Cleanly close the ssh session
    ssh.close()

def cluster_cli_start():
    # Establish an SSH session with paramiko
    ssh = paramiko.SSHClient()
    # Accept ssh key if this is the first time connecting.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Create an ssh connection to the CVM using the user and password supplied above
    ssh.connect(CVM, username=user, password=passwd)
    # Execute the command to start the cluster.  Capture stdin, stdout, and stderr from the command.
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    # Print stdout from the command
    print(ssh_stdout.read().decode())
    # Print stderr from the command
    print(ssh_stderr.read().decode())
    # Cleanly close the ssh session
    ssh.close()

def cluster_cli_stop():
    # command use to stop the cluster
    # "cluster stop" is interactive and "I agree" must be entered to run the command.  This handles the promts and runs the command.
    command = "source /etc/profile; echo 'I agree' | cluster stop"
    answer = "I agree"
    # Establish an SSH session with paramiko
    ssh = paramiko.SSHClient()
    # Accept ssh key if this is the first time connecting.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # Create an ssh connection to the CVM using the user and password supplied above
    ssh.connect(CVM, username=user, password=passwd)
    # Execute the command to stop the cluster.  Capture stdin, stdout, and stderr from the command.
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    # Print stdout from the command
    print(ssh_stdout.read().decode())
    # Print stderr from the command
    print(ssh_stderr.read().decode())
    # Cleanly close the ssh session
    ssh.close()

def start_prism_central():
    # don't worry about invalid certs
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # setup the API request
    # This is API endpoint to change the powerstate of a VM to "on".
    # Update the UUID to the proper value for the Prism Central VM
    # The UUID can be found by using the 100 Level Prism_Element_v2_GET_vms-no_parameters.py
    # The output may be long, you are looking for something like this. note the UUID entry:
    """
    {
            "allow_live_migrate": true,
            "description": "NutanixPrismCentral",
            "gpus_assigned": false,
            "ha_priority": 0,
            "machine_type": "pc",
            "memory_mb": 31744,
            "name": "PrismCentral",
            "num_cores_per_vcpu": 1,
            "num_vcpus": 6,
            "power_state": "off",
            "timezone": "UTC",
            "uuid": "f70018b1-794e-42f6-aa39-0f9048ee335c",
            "vm_features": {
                "AGENT_VM": false,
                "VGA_CONSOLE": true
            },
    """
    endpoint = f"https://{CLUSTER_IP}:{CLUSTER_PORT}/PrismGateway/services/rest/v2.0/vms/f70018b1-794e-42f6-aa39-0f9048ee335c/set_power_state"
    request_headers = {"Content-Type": "application/json", "charset": "utf-8"}
    # transition the power state to "on"
    request_body = {"transition": "on"}

    # Submit the requests and get the output
    try:
        results = requests.post(
            endpoint,
            data=json.dumps(request_body),
            headers=request_headers,
            verify=False,
            auth=HTTPBasicAuth(CLUSTER_USERNAME, CLUSTER_PASSWORD),
        )

        # Print the results of the request
        # It should be a task_uuid for the request to power on the Prism Central VM
        print(json.dumps(results.json(), indent=4, sort_keys=True))

    # Print Errors if any are present
    except Exception as error:
        print(f"ERROR: {error}")
        print(f"Exception: {error.__class__.__name__}")
        sys.exit()

def stop_prism_central():
    # don't worry about invalid certs
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # setup the API request
    # This is API endpoint to change the powerstate of a VM to "ACPI_SHUTDOWN" which should gracefully
    # shutdown and power-off the Prism Central.
    # Update the UUID to the proper value for the Prism Central VM
    # The UUID can be found by using the 100 Level Prism_Element_v2_GET_vms-no_parameters.py
    # The output may be long, you are looking for something like this. note the UUID entry:
    """
    {
            "allow_live_migrate": true,
            "description": "NutanixPrismCentral",
            "gpus_assigned": false,
            "ha_priority": 0,
            "machine_type": "pc",
            "memory_mb": 31744,
            "name": "PrismCentral",
            "num_cores_per_vcpu": 1,
            "num_vcpus": 6,
            "power_state": "off",
            "timezone": "UTC",
            "uuid": "f70018b1-794e-42f6-aa39-0f9048ee335c",
            "vm_features": {
                "AGENT_VM": false,
                "VGA_CONSOLE": true
            },
    """
    endpoint = f"https://{CLUSTER_IP}:{CLUSTER_PORT}/PrismGateway/services/rest/v2.0/vms/f70018b1-794e-42f6-aa39-0f9048ee335c/set_power_state"
    request_headers = {"Content-Type": "application/json", "charset": "utf-8"}
    # Power off Prism Central
    request_body = {"transition": "ACPI_SHUTDOWN"}

    # Submit the requests and get the output
    try:
        results = requests.post(
            endpoint,
            data=json.dumps(request_body),
            headers=request_headers,
            verify=False,
            auth=HTTPBasicAuth(CLUSTER_USERNAME, CLUSTER_PASSWORD),
        )

        # Print the results of the request
        # It should be a task_uuid for the request to power off the Prism Central VM
        print(json.dumps(results.json(), indent=4, sort_keys=True))

    # Print Errors if any are present
    except Exception as error:
        print(f"ERROR: {error}")
        print(f"Exception: {error.__class__.__name__}")
        sys.exit()

def start_cluster():
    # Pass the IPMI IP address, username, password and powerstate to the host_ipmi function
    print("\nStarting Cluster")
    # Start the node using the IPMI interface
    host_ipmi(hosta, usera, passwda, "on")
    # Ping the CVM until it responds
    ping_result = "Starting Ping Test"
    while ping_result != "Network Active":
        # Ping the CVM every 15 seconds until a successful ICMP response is received, then exit.
        ping_result = check_ping()
        sleep(15)
    # Wait 60 seconds once CVM is responsive to ensure it is accepting requests
    sleep(60)
    # Start the cluster
    cluster_cli_start()
    start_prism_central()

def stop_cluster():
    # Need to add code here to stop all VMs
    # newfunction() to stop all VMs
    # Stop Prism Central
    stop_prism_central()
    # wait a few minutes for Prism Central to power off
    # Need to add some code here to confirm it is off
    sleep(300)
    # Stop the cluster
    cluster_cli_stop()
    shutdown_cvm()
    # Pass the IPMI IP address, username, password and powerstate to the host_ipmi function
    print("\Stopping Cluster")
    host_ipmi(hosta, usera, passwda, "off")

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
