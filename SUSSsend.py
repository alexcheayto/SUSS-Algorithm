### SUSSsend.py
# Sends packets A -> B according to a simplified SUSS algorithm

import time
import math

import TCPTools as TCP

log = open("SUSS.log", 'a')

# Network
HOST = '127.0.0.1'
PORT = 9999

# Adjust these to change behavior of nw
totalPkts = 100 # how mae.time()ny pkts to send?
roundLength = 4.0 # Round Length in sec

lastPktSent = 0 # Increments with each pkt
fin = False # True for the final pkt

# SUSS Slow-Start estimation
slowStart = True
roundNum = 0
roundSize = 4 # num pkts in current round
Gi = 4 # Estimate growth rate for current round

# SUSS Phases
def Clock(phaseLength, phasePkts): # Send pkts in a burst
    global fin
    global lastPktSent

    for i in range(lastPktSent, lastPktSent + phasePkts):
        lastPktSent = i
        fin = (i == totalPkts-1)

        # Create a packet, send it and await ACK
        pkt = TCP.Packet(i, FIN=fin)
        TCP.Send(s, pkt, log)
        TCP.Recieve(s, log)

def Guard(endTime): # Wait until a specific time
    guarding = True

    while guarding:
        guarding = time.time() < endTime

def Pace(phaseLength, phasePkts):
    global fin
    global lastPktSent

    for i in range(lastPktSent, lastPktSent + phasePkts):
       
        lastPktSent = i
        fin = (i == totalPkts-1)

        # Create a packet, send it and await ACK
        pkt = TCP.Packet(i, FIN=fin)
        TCP.Send(s, pkt, log)

        starttime = time.time()
        TCP.Recieve(s, log)
        
        ###track and write the time it took for each packet
        if log!=None: truetime = time.time() - starttime
        else:truetime = starttime
        #print(f"TIME TO TAKE {truetime}")
        TCP.printLog(log, f"TIME TO TAKE {truetime}")

        if fin: break # break early if sent last pkt
        else: time.sleep(phaseLength / phasePkts) # pace pkts evenly

# Main
s = TCP.Client(HOST, PORT) # Connect to server
while not fin: # Go until sent all pkts

    roundNum += 1
    print(f"Round {roundNum}: {roundSize}")

    if not slowStart or lastPktSent + roundSize > totalPkts: # exited SS or final round
        Pace(roundLength, roundSize) # Just send pkts evenly
        break

    roundStart = time.time()
    ClockEst = roundStart + roundLength * 1/8 # Benchmark for upcoming clock

    Clock(roundLength * 1/8, int(math.sqrt(roundSize))) # send clock pkts

    ClockActual = time.time() - roundStart # How long was clock phase?
    
    Guard(roundStart + roundLength * 2/8) # Guard phase: wait to give clock phase time

    Pace(roundLength * 6/8, roundSize - int(math.sqrt(roundSize))) # Pace the rest of the pkts

   
    # Gi estimation based on clock phase measurements
    roundSize *= Gi
