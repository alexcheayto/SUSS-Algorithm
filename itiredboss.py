### run_both.py
# Starts both receivers, then launches both senders at the same time
import subprocess
import time
import sys
 
print("Starting receivers...")
suss_recv = subprocess.Popen([sys.executable, "SUSSrecv.py"])
tcp_recv = subprocess.Popen([sys.executable, "TCPrecv.py"])
 
time.sleep(0.5)  # Give receivers a moment to bind their ports
 
print("Launching both senders simultaneously...")
start = time.time()
 
suss_send = subprocess.Popen([sys.executable, "SUSSsend.py"])
tcp_send  = subprocess.Popen([sys.executable, "TCPsend.py"])
 
# Wait for both senders to finish
suss_send.wait()
tcp_send.wait()
 
elapsed = time.time() - start
print(f"\nBoth senders finished in {elapsed:.2f}s")
print("Check SUSS.log and TCP.log to compare results.")
 
# Clean up receivers
suss_recv.terminate()
tcp_recv.terminate()