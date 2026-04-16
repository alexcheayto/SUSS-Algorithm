### TCPsend.py
# Sends packets A -> B using standard TCP-like congestion control
# (Slow Start + AIMD) for comparison against SUSS algorithm

import time

import TCPTools as TCP

log = open("TCP.log", 'a')

# Network
HOST = '127.0.0.1'
PORT = 9999

# Packet config
totalPkts   = 500   # Must match SUSSsend.py
roundLength = 2.0

lastPktSent = 0
fin         = False

cwnd      = 4
ssthresh  = 256
roundNum  = 0

def send_window(window_size):
    """Send window_size packets, waiting for each ACK."""
    global lastPktSent, fin

    pkts_this_round = min(window_size, totalPkts - lastPktSent)

    for i in range(pkts_this_round):
        seq = lastPktSent
        fin = (seq == totalPkts - 1)

        pkt = TCP.Packet(seq, FIN=fin)
        TCP.Send(s, pkt, log)
        TCP.Recieve(s, log)

        lastPktSent += 1

        if fin:
            break


        time.sleep(roundLength / pkts_this_round)
        # print(f"sleplen={roundLength / pkts_this_round}")

#Main
s = TCP.Client(HOST, PORT)

while not fin:
    roundNum += 1
    print(f"=== Round {roundNum} | cwnd={cwnd} | ssthresh={ssthresh} ===")

    if cwnd < ssthresh:
        print("--- Slow Start ---")
    else:
        print("--- Congestion Avoidance (AIMD) ---")

    send_window(cwnd)

    # After each round: grow cwnd
    if cwnd < ssthresh:
        cwnd *= 2          # Slow Start: exponential growth
    else:
        cwnd += 1          # Congestion Avoidance: additive increase
