import socket
import threading


class Jurek(threading.Thread):
    def __init__(self, host, port):
        super().__init__()

        self.host = host
        self.port = port

        self.proxy = socket.socket()

        self.clients = []

    def run_client(self, conn):
        while 1:
            data = conn.recv(4096)
            self.proxy.send(self.clients.index(conn) + data)

    def run_proxy(self, conn):
        while 1:
            data = conn.recv(4096)
            if len(self.clients) <= data[0]:
                self.clients.append(socket.socket())
                self.clients[-1].connect("localhost", 25565)
                threading.Thread(target=self.run_client, args=[self.clients[-1]]).start()
            self.clients[data[0]].send(data[1:])

    def run(self):
        self.proxy.connect((self.host, self.port))
        threading.Thread(target=self.run_proxy, args=[self.proxy]).start()


if __name__ == '__main__':
    Jurek("zyrafal-proxy.herokuapp.com", 25565).run()
