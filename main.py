import ast
import pygame
import sys

from utility import *
from balloons import balloon as b
from towers import tower as t
from projectiles import projectile

pygame.init()

WIDTH = 1000
HEIGHT = 600


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bloons Tower Defense")
        self.fps_font = pygame.font.SysFont("Arial", 18, bold=True)
        self.path = []
        self.load_path()
        self.clock = pygame.time.Clock()

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

    def display_map(self, screen, map_name, divider):
        red_map = self.load_map(map_name, WIDTH / 2 - 15, HEIGHT)
        blue_map = self.load_map(map_name, WIDTH / 2 - 15, HEIGHT)
        divider = pygame.image.load(divider)

        blue_map = pygame.transform.flip(blue_map, True, False)
        divider = pygame.transform.scale(divider, (30, HEIGHT))

        self.screen.blit(red_map, (0, 0))
        self.screen.blit(blue_map, (WIDTH / 2 + 15, 0))
        self.screen.blit(divider, (WIDTH / 2 - 15, 0))

    def update_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = self.fps_font.render(fps, 1, pygame.Color("WHITE"))
        return fps_text

    def can_place_tower(self, middle_pixel_path, point, path_radius, tower_radius):
        closest_point = find_closest_point(middle_pixel_path, point)
        true_distance = euclidian_distance(closest_point, point)
        if true_distance > path_radius + tower_radius:
            return True
        return False

    def run(self):
        bbb = b.Balloon()
        ccc = b.Balloon(k=True)
        ttt = t.Tower(120, 320)
        kkk = t.Tower(200, 320)
        proj = []
        towers = []
        towers.append(ttt)
        towers.append(kkk)
        balloons = []
        balloons.append(bbb)
        balloons.append(ccc)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    coord = (x, y)

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_map(
                self.screen,
                "images/maps/bloon_map_1.png",
                "images/utility/brick_divider.png",
            )

            for balloon in balloons:
                balloon.draw(self.screen)

            for tower in towers:
                tower.draw(self.screen)
                for balloon in balloons:
                    if tower.in_range(balloon):
                        if tower.can_shoot():
                            pr = projectile.Projectile(tower.get_x(), tower.get_y())
                            pr.projectile_target(balloon)
                            proj.append(pr)
                            tower.is_reloading = True
                            break
                tower.reload()

            for pro in proj:
                pro.draw(self.screen)

            self.screen.blit(self.update_fps(), (10, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.load_path()
    game.run()
