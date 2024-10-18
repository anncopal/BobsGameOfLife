import Bob_game
import pygame

myDisplay = pygame.display.Info()
winWidth = myDisplay.current_w-4
winHeight = myDisplay.current_h-210
win = pygame.display.set_mode((winWidth, winHeight))

game = Bob_game.Game(win, winWidth, winHeight)

#set initial speed for bob
bob = game.bobs.sprites()[0]
bob.speedx =  15
bob.speedy = 10

clock = pygame.time.Clock()
fps = 30

for i in range(10*fps):
		clock.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.FINGERDOWN:
				if event.x * winWidth < bob.rect.x:
					if bob.speedx > 0:
						bob.speedx *= -1
					if (event.y * winHeight < bob.rect.y and bob.speedy > 1) or (event.y * winHeight > bob.rect.y and bob.speedy  < 1):
						bob.speedy *= -1
				if event.x * winWidth > bob.rect.x:
					if bob.speedx < 0:
						bob.speedx *= -1
					if (event.y * winHeight < bob.rect.y and bob.speedy > 1) or (event.y * winHeight > bob.rect.y and bob.speedy  < 1):
						bob.speedy *= -1
						
		game.loop(bob)


game_info = Bob_game.GameInfo(bob.energy)
print(game_info.energy)