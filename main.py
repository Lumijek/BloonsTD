import ast
import pygame
import sys
from numpy import random
from utility import *
from utility import _circlepoints
from balloons import balloon as b
from towers import tower as t
from projectiles import projectile
from balloons import redBalloon as rb, blueBalloon as bb
import gameManager

pygame.init()

WIDTH = 1280
HEIGHT = 800
ROUND_COLOR = (207, 163, 21)
TIME_COLOR = (155, 183, 199)
MONEY_COLOR = (220, 220, 220)
ECO_COLOR = (30, 220, 0)
HEALTH_COLOR = (165, 227, 75)


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bloons Tower Defense")
        self.fps_font = pygame.font.SysFont("Arial", 18, bold=True)
        self.text_font = pygame.font.Font("assets/oetztype.ttf", 18, bold=True)
        self.path = []
        self.load_path()
        self.load_images()
        self.clock = pygame.time.Clock()
        self.game_state = gameManager.GameManager()

    def load_path(self):
        lines = []
        with open("assets/map_1.txt", "r") as f:
            for line in f:
                lines.append(line.strip())

        lines = set(lines)
        for coordinate in lines:
            coord = ast.literal_eval(coordinate)
            self.path.append(coord)

    def load_images(self):
        self.red_map = self.load_map(
            "images/maps/bloon_map_1.png", WIDTH / 2 - 15, HEIGHT
        )
        self.blue_map = self.load_map(
            "images/maps/bloon_map_1.png", WIDTH / 2 - 15, HEIGHT
        )
        self.divider = pygame.image.load("images/utility/brick_divider.png")
        self.round_display = pygame.image.load("images/utility/round_bg.png")
        self.game_info_bg = pygame.image.load("images/utility/game_info_bg.png")
        self.red_health_bar = pygame.image.load("images/utility/red_health_bar.png")
        self.green_health_bar = pygame.image.load(
            "images/utility/green_health_bar.png"
        ).convert_alpha()
        self.blue_map = pygame.transform.flip(self.blue_map, True, False)
        self.divider = pygame.transform.scale(self.divider, (30, HEIGHT))
        self.red_health_bar = pygame.transform.scale(
            self.red_health_bar, (WIDTH / 2, HEIGHT / 20)
        )
        self.green_health_bar = pygame.transform.scale(
            self.green_health_bar, (WIDTH * (15 / 32), HEIGHT / 24)
        )
        self.game_info_bg = pygame.transform.scale(
            self.game_info_bg,
            (
                self.game_info_bg.get_width() * 1.35,
                self.game_info_bg.get_height() * 1.4,
            ),
        )

    def load_map(self, map_name, width, height):

        current_map = pygame.image.load(map_name)
        current_map = pygame.transform.scale(current_map, (width, height))
        current_map = pygame.transform.rotate(current_map, 0)

        return current_map

    def display_map(self):
        self.screen.blit(self.red_map, (0, 0))
        self.screen.blit(self.blue_map, (WIDTH / 2 + 15, 0))
        self.screen.blit(self.divider, (WIDTH / 2 - 15, 0))

    def display_images(self, health_ratio):
        self.screen.blit(self.red_health_bar, (0, 0))
        self.green_health_bar = pygame.transform.scale(
            self.green_health_bar, (WIDTH * (15 / 32) * health_ratio, HEIGHT / 24)
        )
        self.screen.blit(self.green_health_bar, (0, 3))
        self.screen.blit(
            self.round_display, (WIDTH / 2 - self.round_display.get_width() / 2, 0)
        )
        self.screen.blit(
            self.game_info_bg,
            (
                WIDTH / 2 - self.game_info_bg.get_width() / 2,
                HEIGHT - self.game_info_bg.get_height(),
            ),
        )
        self.game_state.change_alpha()
        self.green_health_bar.set_alpha(self.game_state.get_alpha())

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.fps_font.render(fps, 1, pygame.Color("WHITE"))
        self.screen.blit(fps_text, (10, 6))

    def can_place_tower(self, middle_pixel_path, point, path_radius, tower_radius):
        closest_point = find_closest_point(middle_pixel_path, point)
        true_distance = euclidian_distance(closest_point, point)
        if true_distance > path_radius + tower_radius:
            return True
        return False

    # Method from https://stackoverflow.com/questions/54363047/how-to-draw-outline-on-the-fontpygame
    def render_text(self, text, font, text_color, outline_color, outline_width):
        text_surface = font.render(text, 1, text_color).convert_alpha()
        width = text_surface.get_width() + 2 * outline_width
        height = font.get_height()

        outline_surface = pygame.Surface(
            (width, height + 2 * outline_width)
        ).convert_alpha()
        outline_surface.fill((0, 0, 0, 0))

        surf = outline_surface.copy()

        outline_surface.blit(
            font.render(text, 1, outline_color).convert_alpha(), (0, 0)
        )

        for dx, dy in _circlepoints(outline_width):
            surf.blit(outline_surface, (dx + outline_width, dy + outline_width))

        surf.blit(text_surface, (outline_width, outline_width))
        return surf

    def randomBalloon(self):
        r = random.uniform(-1, 1)
        if r > 0:
            return rb.RedBalloon()
        else:
            return bb.BlueBalloon()

    def display_game_information(self):
        round_text = self.render_text("Round", self.text_font, ROUND_COLOR, "BLACK", 2)
        self.screen.blit(round_text, (WIDTH / 2 - round_text.get_width() / 2, 0))
        round_number_text = self.render_text(
            str(self.game_state.get_round()), self.text_font, ROUND_COLOR, "BLACK", 2
        )
        self.screen.blit(
            round_number_text,
            (
                (WIDTH / 2) - round_number_text.get_width() / 2,
                round_text.get_height() - 5,
            ),
        )
        time_text = self.render_text(
            str(self.game_state.get_time()), self.text_font, TIME_COLOR, "BLACK", 2
        )
        self.screen.blit(time_text, ((WIDTH / 2) - 15, HEIGHT * (4 / 5)))
        money_text = self.render_text(
            str(self.game_state.get_money()), self.text_font, MONEY_COLOR, "BLACK", 2
        )
        self.screen.blit(money_text, ((WIDTH / 2) - 15, HEIGHT * (6 / 7) - 5))
        eco_text = self.render_text(
            str(self.game_state.get_eco()), self.text_font, ECO_COLOR, "BLACK", 2
        )
        self.screen.blit(eco_text, ((WIDTH / 2) - 15, HEIGHT * (9 / 10)))
        quit_text = self.render_text("Quit?", self.text_font, TIME_COLOR, "BLACK", 2)
        self.screen.blit(
            quit_text, ((WIDTH / 2) - 15, HEIGHT - quit_text.get_height() - 12)
        )
        health_text = self.render_text(
            str(self.game_state.get_health()), self.text_font, HEALTH_COLOR, "BLACK", 2
        )
        self.screen.blit(health_text, (50, 8))

    def run(self):

        proj = []  # projectiles
        towers = []
        balloons = []
        bbb = self.randomBalloon()
        balloons.append(bbb)
        self.game_state.start_round()
        while True:

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:

                    self.game_state.change_round()  # testing purposes
                    self.game_state.change_health(1)  # testing purposes
                    x, y = pygame.mouse.get_pos()
                    ts = t.Tower(x, y)
                    if self.can_place_tower(self.path, (x, y), 20, ts.get_height() / 2):
                        towers.append(t.Tower(x, y))
                    else:
                        del ts

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_map()

            for balloon in balloons:
                balloon.draw(self.screen)

            for tower in towers:
                tower.draw(self.screen)
                for balloon in balloons:
                    if tower.in_range(balloon):
                        if tower.can_shoot():
                            pr = projectile.Projectile(tower.get_x(), tower.get_y())
                            path, path_index = balloon.get_path_details()
                            pr.projectile_target(balloon, path, path_index)
                            proj.append(pr)
                            tower.is_reloading = True
                            break

                tower.reload()

            for i in range(len(proj)):
                proj[i].draw(self.screen)
                if proj[i].projectile_dead():
                    proj[i] = 0

            while 0 in proj:
                proj.remove(0)

            self.display_images(self.game_state.get_player_health_ratio())
            self.display_game_information()
            # self.update_fps()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.load_path()
    game.run()
