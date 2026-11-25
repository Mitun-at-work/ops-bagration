import socket
import select

# 1. Subject (Observable Socket Monitor)
class TCPMonitor:
    def __init__(self):
        self.sockets = {}
        self.observers = []

    def subscribe(self, observer):
        self.observers.append(observer)

    def notify(self, event, conn_id, payload=None):
        for obs in self.observers:
            obs.update(event, conn_id, payload)

    def add_connection(self, conn_id, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.setblocking(False)
        self.sockets[s] = conn_id
        self.notify("OPEN", conn_id)
        return s

    def poll(self, timeout=0.5):
        active = list(self.sockets.keys())
        if not active:
            return
        readable, _, _ = select.select(active, [], [], timeout)
        for s in readable:
            conn_id = self.sockets[s]
            data = s.recv(4096)
            if data:
                self.notify("TRANSFERRING", conn_id, len(data))
            else:
                self.notify("CLOSED", conn_id)
                del self.sockets[s]
                s.close()

# 2. Observers (React independently to socket state changes)
class DashboardObserver:
    def update(self, event, conn_id, payload):
        print(f"[UI Dashboard] Conn #{conn_id} -> {event} ({payload or 0} bytes)")

class AlertObserver:
    def update(self, event, conn_id, payload):
        if event == "CLOSED":
            print(f"[Alert System] Warning: Conn #{conn_id} disconnected!")

# --- Usage ---
monitor = TCPMonitor()
monitor.subscribe(DashboardObserver())
monitor.subscribe(AlertObserver())

s1 = monitor.add_connection(1, "example.com", 80)
s2 = monitor.add_connection(2, "example.com", 80)

s1.send(b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")

for _ in range(5):
    monitor.poll()
