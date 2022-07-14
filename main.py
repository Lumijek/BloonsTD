import ast
import pygame
import sys
from numpy import random
from utility import *
from balloons import balloon as b
from towers import tower as t
from projectiles import projectile
from balloons import redBalloon as rb, blueBalloon as bb
import gameManager

pygame.init()

WIDTH = 1000
HEIGHT = 600
ROUND_COLOR = (242, 187, 65)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bloons Tower Defense")
        self.fps_font = pygame.font.SysFont("Arial", 18, bold=True)
        self.text_font = pygame.font.Font("assets/oetztype.ttf", 18, bold=True)
        self.path = []
        self.load_path()
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

    def load_map(self, map_name, width, height):

        current_map = pygame.image.load(map_name)
        current_map = pygame.transform.scale(current_map, (width, height))
        current_map = pygame.transform.rotate(current_map, 0)

        return current_map

    def display_map(self, screen, map_name, divider, round_displayer):
        red_map = self.load_map(map_name, WIDTH / 2 - 15, HEIGHT)
        blue_map = self.load_map(map_name, WIDTH / 2 - 15, HEIGHT)
        divider = pygame.image.load(divider)
        round_display = pygame.image.load(round_displayer)

        blue_map = pygame.transform.flip(blue_map, True, False)
        divider = pygame.transform.scale(divider, (30, HEIGHT))


        self.screen.blit(red_map, (0, 0))
        self.screen.blit(blue_map, (WIDTH / 2 + 15, 0))
        self.screen.blit(divider, (WIDTH / 2 - 15, 0))
        self.screen.blit(round_display, (WIDTH / 2 - round_display.get_width() / 2, 0))

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.fps_font.render(fps, 1, pygame.Color("WHITE"))
        self.screen.blit(fps_text, (10, 0))

    def can_place_tower(self, middle_pixel_path, point, path_radius, tower_radius):
        closest_point = find_closest_point(middle_pixel_path, point)
        true_distance = euclidian_distance(closest_point, point)
        if true_distance > path_radius + tower_radius:
            return True
        return False

    def randomBalloon(self):
        r = random.uniform(-1, 1)
        if r >0:
            return rb.RedBalloon()
        else:
            return bb.BlueBalloon()

    def display_game_information(self):
        round_text = self.text_font.render("Round", 1, ROUND_COLOR)
        self.screen.blit(round_text, (WIDTH / 2 - round_text.get_width() / 2, 0))
        round_number_text = self.text_font.render(str(self.game_state.get_round()), 1, ROUND_COLOR)
        self.screen.blit(round_number_text, ((WIDTH / 2) - round_number_text.get_width() / 2, 0 + round_text.get_height()))

    def run(self):
        
        proj = [] #projectiles
        towers = []
        balloons = []
        bbb = self.randomBalloon()
        balloons.append(bbb)
        self.game_state.start_round()
        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    ts = t.Tower(x, y)
                    if self.can_place_tower(self.path, (x, y), 20, ts.get_height() / 2):
                        towers.append(t.Tower(x, y))
                    else:
                        del ts

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_map(
                self.screen,
                "images/maps/bloon_map_1.png",
                "images/utility/brick_divider.png",
                "images/utility/round_background.png"
            )

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

            self.display_game_information()
            self.update_fps()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.load_path()
    game.run()
