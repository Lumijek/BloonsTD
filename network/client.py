import socket
import threading
import sys
import os
import signal
import pickle
import pygame
import time
import struct


class Client:
    def __init__(self, host, port, name):
        self.event = threading.Event()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        self.name = name

    def send(self, data):
        try:
            data = pickle.dumps(data)
            length = struct.pack(">I", len(data))
            # self.sock.sendall(length)
            self.sock.sendall(data)
        except Exception as e:
            print("Error sending data.")
            print(e)
            print(data)
            self.sock.close()
            os._exit(1)
            return

    def recv(self):
        try:

            data = self.sock.recv(8192)
            data = pickle.loads(data)
            return data
            if data == "Server shutting down!":
                self.sock.close()
                os._exit(1)
                return
        except Exception as e:
            print(e)
            print("Data:", data)
            self.sock.close()
            os._exit(1)
            return

    def kill_client(self, sig, frame):
        self.sock.sendall("q".encode())
        self.sock.close()
        self.event.set()
        os._exit()

    def start(self):

        name = "BOB"
        self.sock.connect(self.addr)
        self.sock.sendall(name.encode())
        signal.signal(signal.SIGINT, self.kill_client)
        signal.signal(signal.SIGHUP, self.kill_client)
