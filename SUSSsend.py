### SUSSsend.py
# Allows sending packets between Hosts A <-> B, while logging each packet
# Simulates either SUSS or traditional TCP sending behavior

import socket

# Networking
HostA = '10.0.1.1'
HostB = '10.0.2.2'

PORT = 9999 # TODO: idk what port to use, dont think it matters
dest = ''

SUSS = None # Set to true if A -> B, false if B -> A

# Logging
logfile = open("SUSSsend.log", 'a')
logfile.write("--- SUSSsend.py Log ---\n")

def printLog(s:str):
    print(s)
    logfile.write(s+'\n')
# TODO: printlog, showing timestamps and seq# for send pkts / recv acks
# '-> send info'
# '<- recv info'

# TCP Wrappers
def Send(socket, msg): socket.sendall(msg.encode())
def Recieve(socket) -> str: return socket.recv(1024).decode()


# Prompt to set dest to either A or B
while not dest:
    # TODO: Can just get self ip, if A then set dest to B and vice versa.
    dest = input("Enter Destination Host (A/B): ")

    if   dest in ['a','A']: dest = HostA
    elif dest in ['b','B']: dest = HostB
    else                    dest = ''

    if dest:
        SUSS = (dest == HostB) # A -> B uses SUSS, B -> A does not
        dest = socket.gethostbyname(dest)


while True: # Main Loop
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((SERVER_HOST, SERVER_PORT)) # socket for server

    numPkts = int(input("How many packets to send? (try 10): "))
    while numPkts:
        break
        # TODO Send pkts according to SUSS or TCP rules


### TODO: Pseudocode for now
# create some kind of tcp struct that stores the cwnd,
# and also has SUSS info like estimated ceiling
#
# # Server processing
# need some kind of network state struct (perhaps stored on the server
# script) that defines probabilities to randomly drops packets (simulate packet
# loss) and keeps a buffer of pkts that it processes (simulate the real cwnd).
# Process packets once per 100ms or something idk, acking them once 'processed'.
# This allows the ACK clocking to work
#
# # SUSS Algo
# # TODO: see fig7 in the paper
# we have to keep track of various params like expGrowth, cwnd, blue/red ACKS,
# RTT, etc.
