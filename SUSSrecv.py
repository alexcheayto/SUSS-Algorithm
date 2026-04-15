### Server.py
# Listens for connections and ACKs packets sent to it

import socket
import time

import TCPTools as TCP

log = open("SUSS.log", 'a')
log.write("--- SUSS Log ---\n")

# Network
HOST = "127.0.0.1"
PORT = 9999

processDelay = 0.1 # How long to process each pkt (in sec)


# Main
while True:
    s = TCP.Server(HOST, PORT) # Create a server

    seq = 0 # seq counter

    while True:
        time.sleep(processDelay) # Each pkt takes time to process

        recv = TCP.Recieve(s, log)
        if not recv: continue # no data? just wait for more

        recvPkt = TCP.Parse(recv)

        pkt = TCP.Packet(recvPkt[0], client=False) # Create an ACK packet and send it back
        TCP.Send(s, pkt, log)

        lastByte = recvPkt[1][-1:]
        # print (f"lastByte = {lastByte.encode()}") # Debug print
        if lastByte == '\n': break # End connection on newline

    print(f"Connection closed")

