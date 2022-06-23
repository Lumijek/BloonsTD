import ast
import math
import pygame
import sys

pygame.init()

width = 1000
height = 600

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Bloons Tower Defense")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 18, bold=True)
lines = []
with open("assets/map_1.txt", "r") as f:
    for line in f:
        lines.append(line.strip())
lines = set(lines)
path = []
for coordinate in lines:
    coord = ast.literal_eval(coordinate)
    path.append(coord)


def load_map(map_name, width, height):
    current_map = pygame.image.load(map_name)
    current_map = pygame.transform.scale(current_map, (width, height))
    current_map = pygame.transform.rotate(current_map, 0)

    return current_map


def display_map(screen, map_name, divider):
    red_map = load_map(map_name, width / 2 - 15, height)
    blue_map = load_map(map_name, width / 2 - 15, height)
    divider = pygame.image.load(divider)

    blue_map = pygame.transform.flip(blue_map, True, False)
    divider = pygame.transform.scale(divider, (30, height))

    screen.blit(red_map, (0, 0))
    screen.blit(blue_map, (width / 2 + 15, 0))
    screen.blit(divider, (width / 2 - 15, 0))


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("WHITE"))
    return fps_text


def calculate_distance_without_sqrt(point1, point2):
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2  # for speed


def euclidian_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def find_closest_point(middle_pixel_path, point):
    min_distance = 100000000
    closest_point = None
    for position in middle_pixel_path:
        distance = calculate_distance_without_sqrt(position, point)
        if distance < min_distance:
            closest_point = position
            min_distance = distance
    return closest_point


def can_place_tower(middle_pixel_path, point, path_radius, tower_radius):
    # middle_pixel_path = filter_points(middle_pixel_path, point) Filter points to reduce number of points in calculations
    closest_point = find_closest_point(middle_pixel_path, point)
    true_distance = euclidian_distance(closest_point, point)
    if true_distance > path_radius + tower_radius:
        return True
    return False


while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            coord = (x, y)
            print(can_place_tower(path, coord, 25, 0))

        if event.type == pygame.QUIT:
            f.close()
            pygame.quit()
            sys.exit()

    display_map(
        screen, "images/maps/bloon_map_1.png", "images/utility/brick_divider.png"
    )
    screen.blit(update_fps(), (10, 0))
    pygame.display.update()
    clock.tick(60)
