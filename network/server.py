import socket
import threading
import signal
import os
import random
import time
import pickle
from pprint import pprint
import random


class Server:
    def __init__(self, host, port):
        self.event = threading.Event()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.sock.bind(self.addr)
        self.sock.listen(100)
        self.client_queue = {}
        self.connections = {}

    def shut_down_server(self, sig, frame):
        for connection in list(self.client_queue):
            connection.close()
        self.event.set()
        os._exit(1)

    def queue_handler(self):
        while True:
            if len(self.client_queue) > 1:
                player1, player2 = list(self.client_queue)[:2]
                self.connections[player1] = player2
                self.connections[player2] = player1
                player_select = random.uniform(0, 1)
                if player_select > 0.5:
                    player1.sendall(pickle.dumps("one"))
                    player2.sendall(pickle.dumps("two"))
                else:
                    player1.sendall(pickle.dumps("two"))
                    player2.sendall(pickle.dumps("one"))
                player1_thread = threading.Thread(
                    target=self.handle_client, args=(player1,)
                )
                player2_thread = threading.Thread(
                    target=self.handle_client, args=(player2,)
                )
                player1_thread.start()
                player2_thread.start()
                del self.client_queue[player1]
                del self.client_queue[player2]

    def handle_client(self, client):
        while True:
            try:
                data = client.recv(8192)
                if pickle.loads(data) == "q":
                    client.close()
                    return
                self.send(self.connections[client], data)

            except Exception as e:
                client.close()
                return

    def send(self, client, data):
        try:
            client.sendall(data)
        except Exception as e:
            self.sock.close()
            client.close()
            return

    def start(self):
        signal.signal(signal.SIGINT, self.shut_down_server)
        signal.signal(signal.SIGHUP, self.shut_down_server)
        handler = threading.Thread(target=self.queue_handler)
        handler.start()
        while True:
            client_socket, addr = self.sock.accept()
            name = client_socket.recv(128).decode()
            self.client_queue[client_socket] = name
            print(f"{name} ({addr[0]}) has joined the Server.")


if __name__ == "__main__":
    s = Server("localhost", 9000)
    s.start()
