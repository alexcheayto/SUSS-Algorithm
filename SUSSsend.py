### SUSSsend.py
# Sends packets A -> B according to a simplified SUSS algorithm

import time

import TCPTools as TCP

log = open("SUSS.log", 'a')

# Network
HOST = '127.0.0.1'
PORT = 9999

nwSpeed = 2 # Higher number = slower network to start

numPkts = 100
lastPktSent = 0
fin = False # True for the final pkt

# SUSS Slow-Start estimation
roundSize = 1 # num pkts in current round
Gi = 4 # Estimate growth rate for current round

# Main
s = TCP.Client(HOST, PORT)
roundNum = 0
while not fin: # Go until sent all pkts
    roundSize *= Gi
    pace = nwSpeed / roundSize

    roundNum += 1
    print(f"Round {roundNum}: {roundSize}")

    for i in range(lastPktSent, lastPktSent + roundSize):
        fin = (i == numPkts-1)
        pkt = TCP.Packet(i, FIN=fin) # Create a packet

        TCP.Send(s, pkt, log)
        TCP.Recieve(s, log)
        lastPktSent = i

        time.sleep(pace)
        if fin: break # break early if sent last pkt

    # roundTime = how long it actually took vs how long we thought
    # then use that to change Gi
    # if Gi < 2 skip that block ^ and just redo last round with additive increase + 1
