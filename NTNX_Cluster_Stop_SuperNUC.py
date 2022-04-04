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
# command = "/usr/local/nutanix/cluster/bin/cluster stop"
command = "source /etc/profile; echo 'I agree' | cluster stop"
answer = "I agree"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(CVM, username=user, password=passwd)
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
# time.sleep(10)
# ssh_stdin.write(answer + '\n')
# ssh_stdin.flush()
# ssh_stdout.read()
print(ssh_stdout.read().decode())
print(ssh_stderr.read().decode())
ssh.close()
