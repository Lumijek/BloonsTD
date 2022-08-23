from game import player
import time
import threading


class GameManager:
    def __init__(self):
        self.player_1 = player.Player(150, 400, 250)
        self.player_2 = player.Player(150, 400, 250)
        self.game_timer = 0
        self.round = 0
        self.eco_timer = 0
        self.eco_time = 6
        self.last_time_multiple_of_eco_time = None
        self.alpha_count = 0

    def start_round(self):
        self.initial_time = time.perf_counter()
        self.round = 1

    def update_time(self):
        self.game_timer = round(time.perf_counter() - self.initial_time - 0.5)
        if (
            self.game_timer % self.eco_time == 0
            and self.game_timer != self.last_time_multiple_of_eco_time
        ):
            self.player_1.change_money(self.player_1.get_eco())
            self.last_time_multiple_of_eco_time = self.game_timer

    def get_time_elapsed(self):
        return self.game_timer

    def get_time(self):
        self.update_time()
        time_in_seconds = self.game_timer
        minutes = time_in_seconds // 60
        seconds = time_in_seconds % 60
        if seconds < 10:
            seconds = f"0{seconds}"
        if minutes < 10:
            minutes = f"0{minutes}"
        return f"{minutes}:{seconds}"

    def change_round(self):
        self.round += 1

    def get_round(self):
        return self.round

    def get_money(self):
        return f"${str(self.player_1.get_money())}"

    def get_eco(self):
        return f"${str(self.player_1.get_eco())}"

    def get_health(self):
        return str(self.player_1.get_health())

    def get_player_health_ratio(self):
        return self.player_1.get_health_ratio()

    def change_health(self, change):
        self.player_1.change_health(change)
        self.alpha_count = 5

    def change_alpha(self):
        if self.alpha_count != 0:
            self.alpha_count -= 1

    def get_alpha(self):
        return 255 - (47 * self.alpha_count)
