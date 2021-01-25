import socket
import threading
import os


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
    Server("0.0.0.0", int(os.environ.get('PORT', 5000))).run()
