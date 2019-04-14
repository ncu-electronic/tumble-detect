import subprocess
import signal
import os
import time

subp = subprocess.Popen("python3 mmwave.py /dev/ttyACM4 /dev/ttyACM5",shell = True, cwd = '/home/upsquared/mmwave',preexec_fn = os.setsid)
time.sleep(5)
os.killpg(os.getpgid(subp.pid), signal.SIGTERM)  # Send the signal to all the process groups
#subp.terminate();