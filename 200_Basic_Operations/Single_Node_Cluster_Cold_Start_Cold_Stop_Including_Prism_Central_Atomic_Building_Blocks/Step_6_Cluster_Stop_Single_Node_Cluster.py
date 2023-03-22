#!/usr/bin/python
"""
This is an atomic example of logging into a running CVM and stopping the Nutanix Cluster.
This was tested on a single node cluster but should work regardless of the number of nodes in the cluster.
"""

# imports
# paramiko is used for ssh
import paramiko
import time

# Host variables
# CVM IP Address
CVM = "10.0.0.133"
# CVM linux shell username for ssh
user = "nutanix"
# CVM user password.  The example below is the default password for Nutanix installations.
passwd = "nutanix/4u"
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
