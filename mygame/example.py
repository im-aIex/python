import game
import frame

class examplegame(game.game):

	def onstart(self):
		print('*' * 16 + ' - STARTING - ' + '*' * 16)

	def onquit(self, message):
		message += ('Quit from example.py',)
		print message
		print('*' * 16 + ' - QUITING - ' + '*' * 16)

	def logic(self):
		pass

	def render(self):
		pass



class exampleframe(frame.frame):
	pass

if __name__ == '__main__':

	game = examplegame()

	frame = exampleframe(800, 600)

	game.add(frame)
	game.setup()
	game.setfps(60)
	game.run()