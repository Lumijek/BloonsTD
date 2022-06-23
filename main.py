import pygame
import sys

pygame.init()

width = 1000
height = 600

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Bloons Tower Defense")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial" , 18 , bold = True)

def load_map(map_name, width, height):
	current_map = pygame.image.load(map_name)
	current_map = pygame.transform.scale(current_map, (width, height))
	current_map = pygame.transform.rotate(current_map, 0)

	return current_map

def display_map(screen, map_name, divider):
	red_map = load_map(map_name, width/2 - 15, height)
	blue_map = load_map(map_name, width/2 - 15, height)
	divider = pygame.image.load(divider)

	blue_map = pygame.transform.flip(blue_map, True, False)
	divider = pygame.transform.scale(divider, (30, 600))

	screen.blit(red_map, (0, 0))
	screen.blit(blue_map, (width/2 + 15, 0))
	screen.blit(divider, (width/2 - 15, 0))

def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("WHITE"))
	return fps_text

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	display_map(screen, "images/maps/bloon_map_1.png", "images/utility/brick_divider.png")
	screen.blit(update_fps(), (10,0))

	pygame.display.update()
	clock.tick(60)