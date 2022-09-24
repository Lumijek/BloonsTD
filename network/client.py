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
            f = self.sock.makefile(mode='wb')
            pickle.dump(data, f)
            f.close()
        except Exception as e:
            print("close1", time.time())
            print("Error sending data.")
            print(e)
            print(data)
            self.sock.close()
            os._exit(1)
            return

    def recv(self):
        try:
            f = self.sock.makefile(mode='rb')
            unpkl = pickle.Unpickler(f)
            data = unpkl.load()
            f.close()
            return data
            if data == "Server shutting down!":
                self.sock.close()
                os._exit(1)
                return
        except Exception as e:
            print("close2", time.time())
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
