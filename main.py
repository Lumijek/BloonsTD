import ast
from pickle import NONE
from re import I
import pygame
import sys
import time
from numpy import empty, random
from utility import *
from utility import _circlepoints
from balloons import balloon as b
from towers import tower as t
from towers import dartm as dm
from towers import boomerangm as bm
from projectiles import projectile
from balloons import redBalloon as rb, blueBalloon as bb
from balloons import greenBalloon as gb
from balloons import yellowBalloon as yb
from balloons import blackBalloon as blb
import gameManager
import random
import socket
import struct

pygame.init()

WIDTH = 1280
HEIGHT = 800
START_PIXEL = 140
ROUND_COLOR = (207, 163, 21)
TIME_COLOR = (155, 183, 199)
MONEY_COLOR = (220, 220, 220)
ECO_COLOR = (30, 220, 0)
HEALTH_COLOR = (165, 227, 75)

#in the __init__ there will be a player_type (either one or two)
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bloons Tower Defense")
        self.fps_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.text_font = pygame.font.Font("assets/oetztype.ttf", 24, bold=True)
        self.path = []
        self.load_path()
        self.load_images()
        self.clock = pygame.time.Clock()
        self.game_state = gameManager.GameManager()
        self.player_type = "two"
        b.Balloon.PLAYER_TYPE = self.player_type

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
        self.player_1_bg = pygame.image.load(
            "images/utility/player_1_bg.png"
        ).convert_alpha()
        self.player_2_bg = pygame.image.load(
            "images/utility/player_2_bg.png"
        ).convert_alpha()

        self.divider = pygame.image.load("images/utility/brick_divider.png")
        self.round_display = pygame.image.load("images/utility/round_bg.png")
        self.game_info_bg = pygame.image.load("images/utility/game_info_bg.png")
        self.red_health_bar = pygame.image.load("images/utility/red_health_bar.png")
        self.green_health_bar = pygame.image.load(
            "images/utility/green_health_bar.png"
        ).convert_alpha()
        self.blue_map = pygame.transform.flip(self.blue_map, True, False)
        self.player_1_bg = pygame.transform.smoothscale(
            self.player_1_bg, (START_PIXEL, HEIGHT)
        )
        self.player_2_bg = pygame.transform.smoothscale(
            self.player_2_bg, (START_PIXEL, HEIGHT)
        )
        self.divider = pygame.transform.smoothscale(self.divider, (30, HEIGHT))
        self.red_health_bar = pygame.transform.scale(
            self.red_health_bar, (WIDTH / 2 - START_PIXEL, HEIGHT / 20)
        )
        self.green_health_bar = pygame.transform.smoothscale(
            self.green_health_bar, (WIDTH * (15 / 32) - START_PIXEL, HEIGHT / 24)
        )
        self.game_info_bg = pygame.transform.smoothscale(
            self.game_info_bg,
            (
                self.game_info_bg.get_width() * 1.35,
                self.game_info_bg.get_height() * 1.4,
            ),
        )

    def load_map(self, map_name, width, height):

        current_map = pygame.image.load(map_name)
        current_map = pygame.transform.smoothscale(current_map, (485, height))
        current_map = pygame.transform.rotate(current_map, 0)

        return current_map

    def display_map(self):
        self.screen.blit(self.red_map, (START_PIXEL, 0))
        self.screen.blit(self.blue_map, (WIDTH / 2 + 15, 0))
        self.screen.blit(self.divider, (WIDTH / 2 - 15, 0))

    def display_images(self, health_ratio):
        self.screen.blit(self.player_1_bg, (0, 0))
        self.screen.blit(self.player_2_bg, (WIDTH - START_PIXEL, 0))
        self.screen.blit(self.red_health_bar, (START_PIXEL, 0))
        self.green_health_bar = pygame.transform.scale(
            self.green_health_bar,
            ((WIDTH * (15 / 32) - START_PIXEL) * health_ratio, HEIGHT / 24),
        )
        self.screen.blit(self.green_health_bar, (START_PIXEL, 3))
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

    def can_place_tower(self, towers, middle_pixel_path, point, path_radius, tower_radius):
        closest_point = find_closest_point(middle_pixel_path, point)
        true_distance = euclidian_distance(closest_point, point)
        on_tower = False
        for tower in towers:
            if (point[0] - tower.x) ** 2 + (point[1] - tower.y) ** 2 < 20 ** 2:
                on_tower = True
        if true_distance > path_radius + tower_radius and not on_tower:
            if self.player_type == "one":
                if point[0]>=START_PIXEL and point[0] <=WIDTH/2:
                    return True
            else:
                if point[0] >= WIDTH/2 and point[0] <= WIDTH-START_PIXEL:
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

    def inst_balloon(self, start_info):
        rBal = []
        x = start_info[0]
        y = start_info[1]
        balloon_list = start_info[2]
        path_index = start_info[3]
        if balloon_list == None:
            return None
        c = 1
        for i in balloon_list:
            num = int(i[0])
            balloon_id = i[1:]
            if balloon_id == "red":
                for j in range(num):
                    if (path_index%2==0):
                        y = y-(j+c)*10
                    else:
                        x = x-(j+c)*10
                    rBal.append(rb.RedBalloon(x, y, path_index))
            if balloon_id == "blue":
                for j in range(num):
                    if (path_index%2==0):
                        y = y-(j+c)*10
                    else:
                        x = x-(j+c)*10
                    rBal.append(bb.BlueBalloon(x, y, path_index))
            if balloon_id == "green":
                for j in range(num):
                    if path_index%2==0:
                        y = y-(j+c)*10
                    else:
                        x = x-(j+c)*10
                    rBal.append(gb.GreenBalloon(x, y, path_index))
            if balloon_id == "yellow":
                for j in range(num):
                    if path_index%2==0:
                        y = y-(j+c)*10
                    else:
                        x = x-(j+c)*10
                    rBal.append(yb.YellowBalloon(x, y, path_index))
            c+=1
        return rBal

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
        self.screen.blit(health_text, (START_PIXEL + 50, 4))

    def run(self):
        proj = [] 
        towers = []
        balloons = []
        tower_images = {
            "Tower": [t.Tower.img, t.Tower.circ_img],
            "DartMonkey": [dm.DartMonkey.img, dm.DartMonkey.circ_img],
            "BoomerangMonkey": [bm.BoomerangMonkey.img, bm.BoomerangMonkey.circ_img],
        }
        currentTshirt = None
        bbb = gb.GreenBalloon()
        balloons.append(bbb)

        self.game_state.start_round()
        previous_time = time.perf_counter()
        while True:
            delta_time = time.perf_counter() - previous_time
            previous_time = time.perf_counter()

            for event in pygame.event.get():

                if event.type == pygame.KEYDOWN:
                    bbb = blb.BlackBalloon()
                    balloons.append(bbb)
                    if event.key == pygame.K_BACKQUOTE:
                        print("default tower")
                        currentTshirt = "Tower"
                        x, y = pygame.mouse.get_pos()
                        self.screen.blit(
                            t.Tower.img,
                            (
                                x - t.Tower.img.get_width() / 2,
                                y - t.Tower.img.get_height() / 2,
                            ),
                        )
                        circ = t.Tower.circ_img
                        # self.screen.blit(circ,(x - circ.get_width() / 2, y - circ.get_width() / 2))
                    if event.key == pygame.K_1:
                        print("dart")
                        #print(len(towers))
                        currentTshirt = "DartMonkey"
                        x, y = pygame.mouse.get_pos()
                        self.screen.blit(
                            dm.DartMonkey.img,
                            (
                                x - dm.DartMonkey.img.get_width() / 2,
                                y - dm.DartMonkey.img.get_height() / 2,
                            ),
                        )
                    if event.key == pygame.K_2:
                        print("dart")
                        
                        currentTshirt = "BoomerangMonkey"
                        x, y = pygame.mouse.get_pos()
                        self.screen.blit(
                            bm.BoomerangMonkey.img,
                            (
                                x - bm.BoomerangMonkey.img.get_width() / 2,
                                y - bm.BoomerangMonkey.img.get_height() / 2,
                            ),
                        )
                    if event.key == pygame.K_5:
                        balloons.append(blb.BlackBalloon())

                if (event.type == pygame.MOUSEBUTTONDOWN) & (currentTshirt != None):
                    self.game_state.change_round()  # testing purposes
                    #self.game_state.change_health(1)  # testing purposes, not needed rn
                    x, y = pygame.mouse.get_pos()
                    if currentTshirt == "DartMonkey":
                        ts = dm.DartMonkey(x, y)
                    elif currentTshirt == "BoomerangMonkey":
                        ts = bm.BoomerangMonkey(x, y)
                    else :
                        ts = t.Tower(x, y)
                    
                    if self.can_place_tower(towers, self.path, (x, y), 20, ts.get_height() / 2):
                        towers.append(ts)
                    else:
                        del ts
                    currentTshirt = None

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display_map()

            for balloon in balloons:
                balloon.draw(self.screen, delta_time)

            for tower in towers:
                tower.draw(self.screen)
                for balloon in balloons:
                    if tower.in_range(
                        balloon.mask,
                        (
                            balloon.get_x() - balloon.img.get_width() / 2,
                            balloon.get_y() - balloon.img.get_height() / 2,
                        ),
                    ):
                        if tower.can_shoot():
                            pr = projectile.Projectile(
                                tower.get_center_x(), tower.get_center_y()
                            )
                            path, path_index = balloon.get_path_details()
                            if pr.projectile_target(
                                balloon, path, path_index, delta_time
                            ):
                                tower.projFired(pr.angle)
                                proj.append(pr)
                                tower.is_reloading = True
                                break

                tower.reload(delta_time)

            new_balloons = []
            for i in range(len(proj)):
                proj[i].draw(self.screen, delta_time)
                projectile_mask = proj[i].get_mask()
                for balloon in balloons:
                    if balloon.is_collided(
                        projectile_mask,
                        (
                            proj[i].get_x() - proj[i].img.get_width() / 2,
                            proj[i].get_y() - proj[i].img.get_height() / 2,
                        ),
                    ):

                        # proj[i].durability -= 1
                        bL = self.inst_balloon(balloon.is_killed())
                        if bL is not None:
                            for jib in range(len(bL)):
                                new_balloons.append(bL[jib])
                        balloons.remove(balloon)
                        proj[i].kill_projectile()

                if proj[i].projectile_dead():
                    proj[i] = 0
            balloons += new_balloons
            x, y = pygame.mouse.get_pos()
            if currentTshirt != None:
                img, circ_img = tower_images[currentTshirt]
                self.screen.blit(
                    circ_img,
                    (x - circ_img.get_width() / 2, y - circ_img.get_height() / 2),
                )
                self.screen.blit(
                    img, (x - img.get_width() / 2, y - img.get_height() / 2)
                )

            while 0 in proj:
                proj.remove(0)
            self.display_images(self.game_state.get_player_health_ratio())
            self.display_game_information()
            pygame.display.update()
            self.clock.tick(120)

if __name__ == "__main__":
    game = Game()
    game.load_path()
    game.run()
