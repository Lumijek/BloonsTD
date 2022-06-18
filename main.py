import pygame
import sys

pygame.init()

width = 1000
height = 600


screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("Bloons Tower Defense")

clock = pygame.time.Clock()

def load_map(map_name, width, height):
	current_map = pygame.image.load(map_name)
	current_map = pygame.transform.scale(current_map, (width, height))
	return current_map

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	c_map = load_map("images/maps/Monkey_meadow.png", width, height)
	screen.blit(c_map, (0, 0))

	pygame.display.update()
	clock.tick(30)