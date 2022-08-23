from game import main
from network.client import Client

host = "localhost"
port = 9000

client = Client(host, port, "Bob")
player_game = main.Game(client)
player_game.run()
