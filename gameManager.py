import player
import time

class gameManager:
	def __init__(self):
		self.player_1 = player.Player(1, 2, 3)
		self.player_2 = player.Player(1, 2, 3)
		self.game_timer = 0
		self.round = 0

	def start_round(self):
		self.initial_time = time.perf_counter()
		self.round = 1

	def update_time(self):
		self.game_timer = round(time.perf_counter() - self.initial_time)

	def get_time_elapsed(self):
		return self.game_timer

	def time_display(self):
		self.update_time()
		time_in_seconds = self.game_timer
		minutes = time_in_seconds // 60
		seconds = time_in_seconds % 60
		if seconds < 10:
			seconds = f"0{seconds}"
		return f"{minutes}:{seconds}"

	def change_round(self):
		self.round += 1

gm = gameManager()
gm.start_round()
for i in range(100):
	print(gm.time_display())
	time.sleep(1.4)