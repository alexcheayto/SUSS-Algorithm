### TCPTools.py
# Collection of funcs that are useful

import socket

def printLog(logfile, s:str):
    print(s)
    logfile.write(s+'\n')
# TODO: printlog, showing timestamps and seq# for send pkts / recv acks
# '-> send info'
# '<- recv info'

# TCP Wrappers
def Send(socket, msg, log=None):
    socket.sendall(msg.encode())
    if log is not None: printLog(log, f"-> {msg}")

def Recieve(socket, log=None) -> str:
    msg = socket.recv(1024).decode()
    if log is not None: printLog(log, f"<- {msg}")
    return msg

def Server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Enable reuse

    print(f"Server listening on port {PORT}...")
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    return conn
