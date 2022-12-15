#!/usr/bin/python
#
################################################################################
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
command = "/usr/local/nutanix/cluster/bin/cluster start"

def check_ping():
    # Ping the CVM on the first hoes in the tuple with 1 ICMP packet.  A "0", indicating the CVM is active on the network.
    # This is a proxy for verifying the CVM is actually operational.  A better method would be to login to the CVM and
    # run a command like "cluster status", but we are going for simple at this point.
    hostname = nodetuple([0]).cvmip
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
    # 121522 Needs Updating
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
    # 121522 Needs Updating
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
    # 121522 Needs Updating
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
    # 121522 Needs Updating
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
    # 121522 Needs Updating
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

### END PASTE

# Take the passed input variables and boot the node
def host_ipmi(host , user, passwd, mode):
    # 121522 Needs Updating
    args = ['/usr/bin/ipmitool -H '+host+' -I lan -P '+passwd+' -U '+user+' -v power '+mode+'']
    print(args)
    subprocess.run(args, shell=True)

# Run the above host_ipmi command to change the power state for each node to "on"
def start_cluster():
    # 121522 Needs Updating
    print("\nStarting Cluster")
    for node in nodetuple:
        host_ipmi(node.ipmihostip, node.ipmihostip, node.ipmipass, "on")
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
    # NEED TO UPDATE
    # sleep(600)
    # start_prism_central()

# Run the above host_ipmi command to change the power state for each node to "off"
def stop_cluster():
    # 121522 Needs Updating
    # Need to add code here to stop all VMs
    # newfunction() to stop all VMs
    # Stop Prism Central
    # NEED TO UPDATE THIS LATER
    #stop_prism_central()
    # wait a few minutes for Prism Central to power off
    # Need to add some code here to confirm it is off
    # Remove commend after updated above
    # sleep(300)
    # Stop the cluster
    cluster_cli_stop()
    shutdown_cvm()
    # Pass the IPMI IP address, username, password and powerstate to the host_ipmi function
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