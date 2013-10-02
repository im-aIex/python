import pygame
import tools.nonoverridable as non

def nonoverridable(f):
    f.nonoverridable = True
    return f

class game:
	__metaclass__ = non.ToughMeta

	clock = pygame.time.Clock()

	fps = 30
	running, quitmessage = True, ()

	objects = ()

	def onstart(self):
		pass

	def onquit(self, e):
		pass

	def logic(self):
		pass

	def render(self):
		pass

	@nonoverridable
	def tick(self):
		self.logic()
		self.render()

	@nonoverridable
	def quit(self, *e):
		self.running = False
		self.quitmessage = e
	
	@nonoverridable
	def init(self):
		global frame
		import frame
		pygame.init()

	@nonoverridable
	def setup(self):
		self.init()
		global frame
		# size = (sizex, sizey)
		print len(self.objects)
		for obj in self.objects:
			obj.setup()

	@nonoverridable
	def setfps(self, gfps):
		self.fps = gfps

	@nonoverridable
	def run(self):
		try:
			self.onstart()
			while self.running:
				for event in pygame.event.get():
					if pygame.QUIT == event.type:
						self.quit('closed')

				self.clock.tick(self.fps)
				self.tick()

				# if not self.running:
				# 	print 'here'
				# 	self.quit('not running')
		except Exception as e:
			self.quit(e)

		self.onquit(self.quitmessage)

	@nonoverridable
	def add(self, obj):
		self.objects += (obj, )
