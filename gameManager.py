import player
import time


class GameManager:
    def __init__(self):
        self.player_1 = player.Player(200, 500, 250)
        self.player_2 = player.Player(200, 500, 250)
        self.game_timer = 0
        self.round = 0

    def start_round(self):
        self.initial_time = time.perf_counter()
        self.round = 12

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

    def get_round(self):
        return self.round
