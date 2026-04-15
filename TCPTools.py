### TCPTools.py
# Collection of funcs to help emulate TCP functionality

import socket
import random # RNG packet data
import string

# Prints and logs at the same time
def printLog(logfile, s:str):
    print(s)
    logfile.write(s+'\n')
    # TODO: probably log a timestamp before each msg

# Create a Packet with SEQ/ACK number and (optional) data
# pkt format: 000 - abcd
# Client packets have num (SEQ) and data (randomly generated)
# Server packets have num (ACK)
# There is a '-' in between the num and data so the parser can separate them
def Packet(num, client:bool = True, FIN=False) -> str:
    # Packet data is just 4 random letters
    data =  ''.join(random.choice(string.ascii_lowercase) for i in range(4))

    pkt = f"{num} - {data if client else 'ACK'}"
    if FIN: pkt += '\n' # End connection on newline

    return pkt

# Parse a Packet() into its num and data
# pkt format: 000 - abcd
def Parse(pkt):
    if pkt is None or pkt == '':
        raise ValueError("Tried to parse empty pkt!")

    return pkt.split(' - ') # [0] = num, [1] = data

# Send data on a socket
def Send(socket, pkt, log=None):
    socket.sendall(pkt.encode())
    if log is not None: printLog(log, f"-> {pkt}")

# Recieve data from a socket
def Recieve(socket, log=None) -> str:
    pkt = socket.recv(1024).decode()
    if log is not None and pkt != '': printLog(log, f"<- {pkt}")
    return pkt

# Listen on a port for incoming connections
def Server(HOST, PORT):
    # Create a socket, enable reuse (this prevents "port already in use" error)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Wait for incoming connections
    print(f"Server listening on port {PORT}...")
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    # Once connection established, return conn (dont care about addr)
    print(f"Connection from {addr}")
    return conn

# Connect to a server (the server must be running)
def Client(HOST, PORT):
    # Create a socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to a server
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    # Once connection established, return the socket
    return s
