import pygame
import random
import sys
import time

from pygame.math import Vector2

CELLCOUNT = 50
CELLSIZE = 10

FPS = 60

class Fruit:

	def __init__(self):
		self.setPosition()

	# Draw fruit on the window
	def drawFruit(self):
		window = pygame.display.get_surface()
		draw = pygame.Rect(self.pos.x*CELLSIZE, self.pos.y*CELLSIZE, CELLSIZE, CELLSIZE)
		pygame.draw.rect(window,(255,0,0),draw)

	# Change position of fruit after it's eaten by snake
	def setPosition(self):
		self.x = random.randint(0,CELLCOUNT-1)
		self.y = random.randint(0,CELLCOUNT-1)
		self.pos = Vector2(self.x, self.y)


class Snake:

	def __init__(self):
		self.body = [Vector2(CELLCOUNT//2,CELLCOUNT//2), Vector2((CELLCOUNT//2)-1,CELLCOUNT//2), Vector2((CELLCOUNT//2)-2,CELLCOUNT//2)]
		self.dir = Vector2(1,0)

	# Draw snake on the window
	def drawSnake(self):
		window = pygame.display.get_surface()
		for block in self.body:
			draw = pygame.Rect(block.x*CELLSIZE, block.y*CELLSIZE, CELLSIZE, CELLSIZE)
			pygame.draw.rect(window,(41,202,0),draw)

	# Move the snake and update it's position on the window
	def moveSnake(self):
		curBody = self.body[:-1]
		curBody.insert(0,curBody[0] + self.dir)
		self.body = curBody

	# Make the snake larger after it eats a fruit
	def addToSnake(self):
		curBody = self.body
		curBody.insert(0,curBody[0] + self.dir)
		self.body = curBody

	# Change snake'ss direction
	def changeDir(self, vec):
		self.dir = vec


class Game:

	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((CELLCOUNT*CELLSIZE, CELLCOUNT*CELLSIZE))
		pygame.display.set_caption("Snake AI")
		self.clock = pygame.time.Clock()


	# Check if snake collides with food
	def checkFoodCollision(self, snake, fruit):
		if snake.body[0] == fruit.pos:
			fruit.setPosition()
			snake.addToSnake()

	# Return true if snake collides with wall
	def checkWallCollision(self, snake):
		if not 0 <= snake.body[0].x < CELLCOUNT or not 0 <= snake.body[0].y < CELLCOUNT:
			return True
		return False

	# Return true if snake collides with itself
	def checkSelfCollision(self, snake):
		for segment in snake.body[1:]:
			if snake.body[0] == segment:
				return True
		return False

	# Ends the game
	def gameOver(self):
		pygame.display.quit()
		pygame.quit()
		sys.exit()

	def run(self):

		# Create instances for snake and fruit
		snake = Snake()
		fruit = Fruit()

		# Create update event to move the snake and check for changes to game state
		screenUpdate = pygame.USEREVENT
		pygame.time.set_timer(screenUpdate, 90)

		# Game loop
		while True:

			for event in pygame.event.get():

				# Close pygame if window is closed
				if event.type == pygame.QUIT:
					pygame.display.quit()
					pygame.quit()
					sys.exit()

				# Update event previously created
				if event.type == screenUpdate:
					self.checkFoodCollision(snake,fruit)
					if self.checkWallCollision(snake) or self.checkSelfCollision(snake):
						self.gameOver()
					snake.moveSnake()

				# Read player input
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_UP and snake.dir != Vector2(0,1):
						snake.changeDir(Vector2(0,-1))
					if event.key == pygame.K_DOWN and snake.dir != Vector2(0,-1):
						snake.changeDir(Vector2(0,1))
					if event.key == pygame.K_LEFT and snake.dir !=  Vector2(1,0):
						snake.changeDir(Vector2(-1,0))
					if event.key == pygame.K_RIGHT and snake.dir != Vector2(-1,0):
						snake.changeDir(Vector2(1,0))

			self.window.fill('black')
			snake.drawSnake()
			fruit.drawFruit()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == "__main__":
	game = Game()
	game.run()
