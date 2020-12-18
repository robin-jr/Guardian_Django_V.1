import os
import signal
import subprocess

command = "netstat -ltnp | grep 9090"
c = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
stdout, stderr = c.communicate()
pid = int(stdout.decode().strip().split(' ')[-1].split('/')[0])
os.kill(pid, signal.SIGTERM)
