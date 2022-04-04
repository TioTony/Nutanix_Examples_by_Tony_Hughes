#!/usr/bin/python
#
################################################################################
#
# This script was written by Tony Hughes for personal use.
#
# Created 4/4/2022
#
# This script does a "cluster start"
#
################################################################################

# imports
import paramiko
import time

# Host variables (read from file in the future)
CVM = "10.0.0.133"
user = "nutanix"
passwd = "nutanix/4u"
command = "sudo shutdown -P now"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(CVM, username=user, password=passwd)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
print(ssh_stdout.read().decode())
print(ssh_stderr.read().decode())
ssh.close()
