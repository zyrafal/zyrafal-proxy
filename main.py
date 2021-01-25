import socket
import threading
import os


class Proxy(threading.Thread):
    def __init__(self, host, port):
        super().__init__()

        self.host = host
        self.port = port

        self.server = socket.socket()
        self.proxy = socket.socket()
        self.client = None

        self.server.bind((self.host, self.port))
        self.server.listen(10)

    def run_proxy(self, conn):
        while 1:
            data = conn.recv(4096)
            self.client.send(data)

    def run_client(self, conn):
        while 1:
            data = conn.recv(4096)
            self.proxy.send(data)

    def run(self):
        print("Waiting for connections...")
        while 1:
            conn, addr = self.server.accept()
            print('Client connected with ' + addr[0] + ':' + str(addr[1]))
            self.client = conn

            target = conn.recv(4096)
            ip = ".".join([str(int(target[i])) for i in range(4)])
            port = int(target[4]) * 256 + int(target[5])
            self.proxy.connect((ip, port))

            print("Target is " + ip + ":" + str(port))

            threading.Thread(target=self.run_client, args=[conn]).start()
            threading.Thread(target=self.run_proxy, args=[self.proxy]).start()


class Server(threading.Thread):
    def __init__(self, host, port):
        super().__init__()

        self.host = host
        self.port = port

        self.server = socket.socket()

        self.jurek = None
        self.clients = []

        self.server.bind((self.host, self.port))
        self.server.listen(10)

    def run_jurek(self, conn):
        while 1:
            data = conn.recv(4096)
            self.clients[data[0]].send(data[1:])

    def run_client(self, conn):
        while 1:
            data = conn.recv(4096)
            self.jurek.send(self.clients.index(conn) + data)

    def run(self):
        print("Waiting for connections...")
        while 1:
            conn, addr = self.server.accept()
            if self.jurek:
                print('Client connected with ' + addr[0] + ':' + str(addr[1]))
                self.clients.append(conn)
                threading.Thread(target=self.run_client, args=[conn]).start()
            else:
                print('Jurek connected with ' + addr[0] + ':' + str(addr[1]))
                self.jurek = conn
                threading.Thread(target=self.run_jurek, args=[conn]).start()


if __name__ == '__main__':
    # Server("0.0.0.0", int(os.environ.get('PORT', 5000))).run()
    Proxy("0.0.0.0", int(os.environ.get('PORT', 5000))).run()
