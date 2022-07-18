import socket
import struct
import sys
import pygame
import time

WIDTH = 1280
HEIGHT = 800
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Server")


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = "localhost"
port = 8000

sock.bind((host, port))
sock.listen()
def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data
conn, addr = sock.accept()
total_time = 0
n = 0
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	t = time.perf_counter()
	data = recv_msg(conn)
	total_time += time.perf_counter() - t
	game_screen = pygame.image.fromstring(bytes(data), (WIDTH, HEIGHT), "RGB")
	screen.blit(game_screen, (0, 0))
	pygame.display.update()
	n += 1
	#if n == 420:
	#	break
print(total_time)
