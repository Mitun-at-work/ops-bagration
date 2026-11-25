import socket
import select
import time

HOST = "example.com"
PORT = 80
NUM_CONNECTIONS = 5

# Track state and byte counts for each socket
connections = {}

for i in range(NUM_CONNECTIONS):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.setblocking(False)  # Required so select() never freezes the loop
    connections[s] = {
        "id": i + 1,
        "local_port": s.getsockname()[1],
        "status": "OPEN (IDLE)",
        "bytes_sent": 0,
        "bytes_recv": 0
    }

# Send data on Connection #1 and #3 to see them transfer data
for s, info in connections.items():
    if info["id"] in (1, 3):
        req = f"GET / HTTP/1.1\r\nHost: {HOST}\r\nConnection: close\r\n\r\n".encode()
        sent = s.send(req)
        info["bytes_sent"] += sent
        info["status"] = "TRANSFERRING (SENT)"

# Monitor all sockets for 5 seconds
end_time = time.time() + 5
while time.time() < end_time:
    # Only pass sockets that haven't been closed yet
    active_sockets = [s for s, info in connections.items() if info["status"] != "CLOSED"]
    if not active_sockets:
        break

    # Ask the OS which sockets have data ready to read (or a disconnect signal)
    readable, _, _ = select.select(active_sockets, [], [], 0.5)

    for s in readable:
        info = connections[s]
        try:
            data = s.recv(4096)
            if data:
                info["bytes_recv"] += len(data)
                info["status"] = "TRANSFERRING (RECEIVING)"
            else:
                # 0 bytes returned by recv() means the server sent a FIN (closed connection)
                info["status"] = "CLOSED"
                s.close()
        except BlockingIOError:
            pass
        except ConnectionResetError:
            info["status"] = "CLOSED (RESET)"
            s.close()

    # Print live dashboard
    print("\n--- Live Socket Status ---")
    for info in connections.values():
        print(f"Conn #{info['id']} (Port {info['local_port']}): {info['status']} | "
              f"Sent: {info['bytes_sent']}B | Recv: {info['bytes_recv']}B")
    time.sleep(1)

# Clean up any remaining open sockets
for s, info in connections.items():
    if info["status"] != "CLOSED":
        s.close()
