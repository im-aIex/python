import pygame
import tools.nonoveridable as non

def nonoveridable(f):
    f.non_overridable = True
    return f

class game:
	__metaclass__ = non.ToughMeta

	clock = pygame.time.Clock()

	fps = 30
	running, quitmessage = True, ()

	def setfps(self, gfps):
		self.fps = gfps

	def onquit(self, e):
		pass

	def tick(self):
		pass

	@nonoveridable
	def quit(self, *e):
		print e
		self.running = False
		self.quitmessage = (e,)
	
	@nonoveridable
	def init(self):
		global myscreen
		import screen as myscreen
		pygame.init()

	@nonoveridable
	def setup(self, sizex, sizey):
		self.init()
		global myscreen
		size = (sizex, sizey)
		myscreen.setup(size)

	@nonoveridable
	def run(self):
		try:
			while self.running:
				for event in pygame.event.get():
					if pygame.QUIT == event.type:
						self.running = False

				self.clock.tick(self.fps)
				self.tick()

				if not self.running:
					print 'here'
					self.quit('not running')
		except Exception as e:
			self.quit(e)

		self.onquit()
