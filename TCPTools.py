### TCPTools.py
# Collection of funcs that are useful

import socket

def printLog(s:str):
    print(s)
    logfile.write(s+'\n')
# TODO: printlog, showing timestamps and seq# for send pkts / recv acks
# '-> send info'
# '<- recv info'

# TCP Wrappers
def Send(socket, msg): socket.sendall(msg.encode())
def Recieve(socket) -> str: return socket.recv(1024).decode()
