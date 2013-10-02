import pygame

class frame:
	
	size = (50, 50)

	screens, currentscreen = (), None

	def __init__(self, sizex = 800, sizey = 600):
		self.size = (sizex, sizey)

	def setup(self):
		frame = pygame.display.set_mode(self.size)