# Client.py

import socket
import time

import TCPTools as TCP

HOST = "127.0.0.1"
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    i = 0
    for letter in "bruh\n":
        s.send(f"SEQ {i} {letter}".encode())
        print(f"-> SEQ {i} {letter}")

        time.sleep(0.5)

        data = s.recv(1024)
        print(f"<- {data}")

        i += 1

