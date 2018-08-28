from singleton import Singleton
from command import Command
import pygame
from pygame.locals import *

LEFT	= -1
STAND	= 0
RIGHT	= 1

class commandJump(Command):
	def execute(self, player):
		return player.getChampion()._tryJump()

class commandAttack(Command):
	def execute(self, player):
		if player.getChampion().checkRadius(player.getRival().getRect()):
			player.getRival()._onHit(player.getChampion()._tryAttack())
		else:
			player.getChampion()._tryAttack()
		return player.getChampion()._onAttack()

class commandMoveLeft(Command):
	def execute(self, player):
		player.setDirection(LEFT)
		return player.getChampion()._tryMove(LEFT)

class commandMoveRight(Command):
	def execute(self, player):
		player.setDirection(RIGHT)
		return player.getChampion()._tryMove(RIGHT)

class inputHandler:
	def __init__(self,player, buttons):
		self.___buttons	= buttons
		self.__player	= player
		self.__buttonA	= commandJump()
		self.__buttonB	= commandMoveLeft()
		self.__buttonC	= commandMoveRight()
		self.__buttonD	= commandAttack()

	def handle(self, keys):
		result = self.__player.getChampion()._onStand()
		self.__player.setDirection(STAND)
		if keys[self.___buttons[0]]==1:
			self.__buttonA.execute(self.__player)
		if keys[self.___buttons[1]]==1:
			result = self.__buttonB.execute(self.__player)
		if keys[self.___buttons[2]]==1:
			result = self.__buttonC.execute(self.__player)
		if keys[self.___buttons[3]]==1:
			result = self.__buttonD.execute(self.__player)
		return result

class Player(metaclass=Singleton):
	def __init__(self, champion, name="Player1"):
		self.__name			= name
		self.__direction	= 0
		self.__render		= None
		self.__champion		= champion
		self.__rival		= None
		self.__buttons		= [K_UP,K_LEFT,K_RIGHT,K_SPACE]
		self.__input_handler= inputHandler(self,self.__buttons)

	def setName(self, name):
		self.__name = name

	def setChampion(self, champion):
		if self.__champion is None:
			self.__champion = champion

	def getChampion(self):
		return self.__champion

	def setRival(self, rival):
		self.__rival = rival

	def getRival(self):
		return self.__rival

	def setDirection(self,direction):
		self.__direction = direction

	def update(self,keystate=None):
		if keystate is not None:
			self.__render = self.__input_handler.handle(keystate)
		else:
			if self.__direction == 0:
				self.__render = self.__champion._onStand()
			else:
				self.__render = self.__champion._tryMove(self.__direction)

			self.__render = self.__champion._onAttack()
			self.__render = self.__champion._onHit()
			self.__render = self.__champion._onDie()
		return self.__render
