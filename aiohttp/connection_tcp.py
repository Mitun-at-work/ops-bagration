import socket
import time

HOST = "example.com"  # Replace with any server or "127.0.0.1" for a local server
PORT = 80             # 80 for HTTP, 443 for HTTPS
NUM_CONNECTIONS = 6

sockets = []

for i in range(NUM_CONNECTIONS):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))  # Performs the TCP 3-way handshake
    sockets.append(s)
    print(f"Connection {i+1} ESTABLISHED | Local port: {s.getsockname()[1]}")

print("\nAll 6 TCP connections are open! Holding for 30 seconds...")
time.sleep(30)

# Cleanly close all connections
for s in sockets:
    s.close()
print("All connections closed.")