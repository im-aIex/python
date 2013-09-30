import mygame

class examplegame(mygame.game):

	def onquit(self, message):
#		message += ('Quit from example.py',)
		print message

	def tick(self):
		pass

if __name__ == '__main__':
	game = examplegame()
	game.setup(800,600)
	game.setfps(60)
	game.run()