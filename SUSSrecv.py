### SUSSrecv.py
# Recieves pkts from SUSSsend.py and processes them with defined NW conditions.

import TCPTools.py

# Networking
HostA = '10.0.1.1'
HostB = '10.0.2.2'

# Server
processDelay = 100 # Processing time per pkt (in ms)
queueSize = 40 # How many packets to queue before dropping?
lossRate = 0.01 # How likely is packet loss?

# Logging
logfile = open("SUSSrecv.log", 'a')
logfile.write("--- SUSSrecv.py Log ---\n")



# TODO: await connection
# Once conn established, print a message and enter main loop

while True: # Main Loop


### TODO: Pseudocode for now

