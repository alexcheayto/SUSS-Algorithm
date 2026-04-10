# Server.py

import socket
import time

HOST = "127.0.0.1"
PORT = 9999

while True: # Main loop
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Enable reuse

        print(f"Listening on port {PORT}")
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print(f"Connection from {addr}")
            while True:
                time.sleep(0.5)
                data = conn.recv(1024)

                if not data: continue
                print(f"<- {data.decode()}")

                conn.sendall(f"ACK {data}".encode())
                print(f"-> ACK {data.decode()}")

                print (f"datalast = {data[-1:]}")
                if data[-1:] == '\n'.encode(): break # End connection on newline

        print(f"Connection closed from {addr}")
