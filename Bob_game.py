import pygame
import random
import math
from bob import Bob
from block import Block

pygame.init()

class GameInfo:
	def __init__(self, energy):
		self.energy = energy


class Game:
	# color
	white= (255, 255, 255)
	black = (0, 0, 0)
	red = (255, 0 ,0)
	blue = (0, 0, 255)
	colors = [red, black, blue]
	
	# Fonts
	scorefont = pygame.font.SysFont("comicsans", 70, True)
	messagefont = pygame.font.SysFont("comicsans", 50, True)

	def __init__(self, window, winWidth, winHeight):		
		self.window = window
		self.winWidth = winWidth
		self.winHeight = winHeight
		self.counter = 0
		self.bestscore = 0
		self.bestrun = 0
		
		self.totalbobs = 1
		self.totalfood = 40
		self.bob_startx = 150
		self.bob_starty = 250 

		self.bobs = pygame.sprite.Group()
		self.foodsupply = pygame.sprite.Group()
		self.frame_vert = pygame.sprite.Group()
		self.frame_hor = pygame.sprite.Group()
		self.new_food_required = False
		
		for i in range (self.totalfood):
			x, y, r ,color  = self.random_parameters()
			r = 20
			self.create_food(x, y, r, self.black)
			
		for i in range (self.totalbobs):
			name = "Bob_" + str(i)
			self.create_bob(self.bob_startx, self.bob_starty, 50, self.red, 0, 0, name)

		# create frame
		self.create_framepart(0, 0, 5, self.winHeight, self.frame_vert)
		self.create_framepart(self.winWidth, 0, 5,self.winHeight, self.frame_vert)
		self.create_framepart(0, 0, self.winWidth, 5, self.frame_hor)
		self.create_framepart(0, self.winHeight, self.winWidth, 5, self.frame_hor)
		
		# generate random sprite parameters
	def random_parameters(self):
		randr = random.randrange(20, 40)
		randx = random.randrange(50, self.winWidth-50)
		randy = random.randrange(50, self.winHeight-50)
		randcolor = self.colors[random.randrange(0,len(self.colors))]
		return randx, randy, randr, randcolor

	 # generate game boundary frames
	def create_framepart(self, x, y, w, h,frame_group):
		new_framepart = Block(w, h)
		new_framepart.rect.x = x
		new_framepart.rect.y = y
		frame_group.add(new_framepart)	
			
	# create a bob, add it to sprite group
	def create_bob(self, x, y, r, color, speedx, speedy, name):
		new_bob = Bob(x, y, r, color, speedx, speedy, 0)
		new_bob.rect.x = x
		new_bob.rect.y = y
		new_bob.name = "Bob_" + str(name)
		self.bobs.add(new_bob)

	# create a food, add to sprite group
	def create_food(self, x, y, r, color):
		new_food = Bob(x, y, r, color, 0, 0, 4)
		new_food.rect.x = x
		new_food.rect.y = y
		self.foodsupply.add(new_food)

	
	# determine location of all food
	def find_food(self, bob):
		foodview = []
		for food in self.foodsupply:
			fdis = math.dist([bob.rect.x, bob.rect.y], [food.rect.x, food.rect.y])
			fdirx = (food.rect.x - bob.rect.x)/fdis
			fdiry = (food.rect.y - bob.rect.y)/fdis				
			foodview.append([fdis, fdirx, fdiry])
		foodview.sort()
		return foodview
		
		
	#detect wall collisions
	def check_walls(self, bob):
		if pygame.sprite.spritecollide(bob, self.frame_hor, False):
		    bob.speedy *= -1
		    if bob.speedy > 0:  # hit top
		        bob.rect.y = self.frame_hor.sprites()[0].rect.bottom
		    else:  # hit buttom
		        bob.rect.y = self.frame_hor.sprites()[1].rect.top - bob.rect.height

		if pygame.sprite.spritecollide(bob, self.frame_vert, False):
		    bob.speedx *= -1 
		    if bob.speedx > 0:  # hit left
		        bob.rect.x = self.frame_vert.sprites()[0].rect.right
		    else:  # hit right
		        bob.rect.x = self.frame_vert.sprites()[1].rect.left - bob.rect.width
		        
	# detect food eaten
	def detect_food_eaten(self, bob):
	   if pygame.sprite.spritecollide(bob, self.foodsupply, True):
	   	bob.foodconsumption += 1
	   	self.new_food_required = True
	   	bob.energy += 1

	# single game loop
	def loop(self, bob):
		bob.move()
		self.check_walls(bob)
		self.detect_food_eaten(bob)
		
		# Check need to resupply food
		if self.new_food_required == True:
			required = self.totalfood-len(self.foodsupply.sprites())
			for i in range (required):
			 		x, y, r, color = self.random_parameters()
			 		r = 20
			 		self.create_food(x, y, r, color)
			self.new_food_required = False
		
		# Render elements of the game
		self.window.fill((50, 50, 50))
		self.bobs.update()
		self.bobs.draw(self.window)
		self.foodsupply.draw(self.window)
		self.frame_vert.draw(self.window)
		self.frame_hor.draw(self.window)
		
#		count_text = self.scorefont.render(("Counter: " + str(self.counter)), 1, (0, 255, 0))
#		energy_text = self.scorefont.render(("Energy: " + str(bob.energy)), 1, (0, 255, 0))
		
		if bob.energy > self.bestscore:
			self.bestscore = bob.energy
			self.bestrun = self.counter
			
#		best_text = self.scorefont.render(("Best: " + str(self.bestscore)), 1, (0, 255, 0))	
		
		total_text = self.scorefont.render(("Count: " + str(self.counter) + "   Energy: " + str(bob.energy) + "   Best: " + str(self.bestscore) + "   Run: " + str(self.bestrun)), 1, (0, 255, 0))
		
#		self.window.blit(count_text, (30, 30))
#		self.window.blit(energy_text, (550, 30))
#		self.window.blit(best_text, (850, 30))
		self.window.blit(total_text, (30, 30))
		
		pygame.display.flip()