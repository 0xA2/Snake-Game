import pygame
import sys
import random
import time

field_size = 500
block = 10
difficulty_level = 10
score = 0
window = pygame.display.set_mode((500,500))
clock = pygame.time.Clock()

class Snake():

	def   __init__(self):
		self.curdir = "RIGHT"
		self.position = [field_size/2, field_size/2]
		self.body = [[field_size/2,field_size/2],[(field_size/2)-10, field_size/2],[(field_size/2)-20,field_size/2]]
		#self.changeDirection = self.curdir

	def changeDir(self, newdir):
		if newdir == "RIGHT" and not self.curdir == "LEFT":
			self.curdir = "RIGHT"
		elif newdir == "LEFT" and not self.curdir == "RIGHT":
			self.curdir = "LEFT"
		elif newdir == "UP" and not self.curdir == "DOWN":
			self.curdir = "UP"
		elif newdir == "DOWN" and not self.curdir == "UP":
			self.curdir = "DOWN"

	def foodCollisionCheck(self,foodhere):
		if self.curdir == "RIGHT":
			self.position[0] += block
		if self.curdir == "LEFT":
			self.position[0]-= block
		if self.curdir == "UP":
			self.position[1] -= block
		if self.curdir == "DOWN":
			self.position[1] += block
		self.body.insert(0,list(self.position))
		if self.position == foodhere:
			return True
		else:
			self.body.pop()
			return False

	def wallCollisionCheck(self):
		if self.position[0] >= field_size or self.position[0] <= 0:
			return True

		elif self.position[1] >= field_size or self.position[1] <= 0:
			return True

		else:
			return False

	def selfCollisionCheck(self):
		for bodysegment in self.body[1:]:
			if self.position == bodysegment:
				return True
		return False

	def getHead(self):
		return self.position

	def getBody(self):
		return self.body

class Food():

	def __init__(self):
		self.position = [random.randrange(1,field_size/block)*block, random.randrange(1,field_size/block)*block]
		self.foodpresent = True

	def spawnfood(self):
		if self.foodpresent == False:
			if self.position == snake.position:
				self.position = [random.randrange(1,field_size/block)*block, random.randrange(1,field_size/block)*block]
			self.foodpresent = True
		return self.position

	def setfood(self, boolean):
		self.foodpresent = boolean

snake = Snake()
food = Food()

def gameover(score):
	pygame.quit()
	print("You scored > " + str(score))
	sys.exit(0)

while True:
	if snake.wallCollisionCheck() or snake.selfCollisionCheck():
		gameover(score)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameover()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				snake.changeDir("RIGHT")
			elif event.key == pygame.K_LEFT:
				snake.changeDir("LEFT")
			elif event.key == pygame.K_UP:
				snake.changeDir("UP")
			elif event.key == pygame.K_DOWN:
				snake.changeDir("DOWN")

	foodposition = food.spawnfood()
	if (snake.foodCollisionCheck(foodposition)):
		score += 1
		food.setfood(False)

	window.fill(pygame.Color(0,0,0))
	for bodysegment in snake.getBody():
		pygame.draw.rect(window, pygame.Color(255,255,255), pygame.Rect(bodysegment[0], bodysegment[1], 10, 10)) 

	pygame.draw.rect(window, pygame.Color(225,0,0), pygame.Rect(foodposition[0], foodposition[1], 10, 10))
	pygame.display.set_caption("Snake in Python? Ironic | Score > " + str(score))
	pygame.display.flip()
	clock.tick(difficulty_level)

