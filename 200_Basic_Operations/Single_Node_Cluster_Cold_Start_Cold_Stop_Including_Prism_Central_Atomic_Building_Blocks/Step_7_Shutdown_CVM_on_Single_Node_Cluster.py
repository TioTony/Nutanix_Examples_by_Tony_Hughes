#!/usr/bin/python
"""
Shutdown the CVM after the cluster has been stopped.
This script has no guardrails.  Make sure you ran Steps 5 and 6 to stop Prism Central and the cluster before running this.
"""

# imports
import paramiko
import time

# Host variables
# CVM IP Address
CVM = "10.0.0.133"
# CVM linux shell username for ssh
user = "nutanix"
# CVM user password.  The example below is the default password for Nutanix installations.
passwd = "nutanix/4u"
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
