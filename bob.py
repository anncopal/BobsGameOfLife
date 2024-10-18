import pygame

white = (255, 255, 255)

class Bob (pygame.sprite.Sprite):
 def __init__ (self, x, y, radius, color, speedx, speedy, border):
   super().__init__()
   
   self.x = x
   self.y = y
   self.radius = radius
   self.color = color
   self.speedx = speedx
   self.speedy = speedy
   self.border = border
   self.collisioncount = 0
   self.foodconsumption = 0
   self.name = "Bobby"
   self.energy = 0
   
   self.image = pygame.Surface([self.radius, self.radius])
   self.image.fill(white)
   self.image.set_colorkey(white)
   
   self.draw_ellipse()
   
   self.rect = self.image.get_rect()
   
 def draw_ellipse(self):
     self.image.fill(white)
     pygame.draw.ellipse(self.image, self.color, [0, 0, self.radius, self.radius], self.border)

 def update_color(self, new_color):
     self.color = new_color
     self.draw_ellipse()
     #print("colorchange: ", self.name, self.rect)
 

 def update_size(self, change):
 	self.size = self.image.get_size()
 	oldx = self.rect.x
 	oldy = self.rect.y
 	image_scaled = pygame.transform.scale(self.image, (int(self.size[0]+change), (int(self.size[1]+change))))
 	self.image = image_scaled
 	self.rect=self.image.get_rect()
 	self.radius = self.rect[3]
 	self.rect.x = oldx
 	self.rect.y = oldy
 	self.draw_ellipse()
 	#print("sizechange: ", self.name, self.rect)
 	
 def move(self):
 	self.rect.x += self.speedx
 	self.rect.y += self.speedy

 
 def collision(self):
     #print("collision: ", self.name, self.rect)
     self.collisioncount +=1
     r, g, b = self.color
     if r >= 5:
     	r -= 5
     if g >= 5:
     	g -= 5
     if b >=5:
     	b -= 5
     new_color = (r, g, b)
     self.update_color(new_color)