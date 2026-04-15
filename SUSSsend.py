### SUSSsend.py
# Sends packets A -> B according to a simplified SUSS algorithm

import time

import TCPTools as TCP

HOST = '127.0.0.1'
PORT = 9999

log = open("SUSS.log", 'a')

# TODO: Custom input size
# int(input("How many pkts to send? "))
numPkts = 10

# G

s = TCP.Client(HOST, PORT)

for i in range(numPkts):
    time.sleep(0.5)

    pkt = TCP.Packet(i, FIN=(i == numPkts-1)) # Create a packet

    TCP.Send(s, pkt, log)
    TCP.Recieve(s, log)

