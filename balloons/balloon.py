import ast
import math
import pygame

class Balloon:
	def __init__(self):
		self.health = 1
		self.velocity = 1
		self.img = pygame.image.load("images/balloon_images/bb.png")
		self.path = []
		self.load()
		self.x = self.path[0][0]
		self.y = self.path[0][1]
		self.path_index = 0
		self.move_distance = 0



	def load(self):
		path_coords = []
		with open("balloons/path.txt", "r") as f:
			for line in f:
				path_coords.append(line.strip())
		for coord in path_coords:
			self.path.append(ast.literal_eval(coord))

	def decrease_health(self, health_change):
		self.health -= health_change


	def draw(self, screen):
		screen.blit(self.img, (self.x - 11, self.y - 11))
		self.move()

	def show_path(self):
		return self.path

	def move(self):
		x1, y1 = self.path[self.path_index]
		x2, y2 = self.path[self.path_index + 1]

		changex = x2 - x1
		changey = y2 - y1
		angle = math.atan2(changey, changex)

		self.x += math.cos(angle) * self.velocity
		self.y += math.sin(angle) * self.velocity

		if round(self.x) == x2 and round(self.y) == y2:
			self.path_index += 1

	def getX(self):
		return self.x
	def getY(self):
		return self.y

		