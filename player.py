from singleton import Singleton
from command import Command
import pygame
from pygame.locals import *

LEFT	= -1
STAND	= 0
RIGHT	= 1

class commandJump(Command):
	def execute(self, player):
		return player.getChampion().jump()

class commandAttack(Command):
	def execute(self, player):
		if player.getChampion().checkRadius(player.getRival().getRect()):
			player.getRival().onHit(player.getChampion().attack())
		else:
			player.getChampion().attack()
		return player.getChampion().onAttack()

class commandMoveLeft(Command):
	def execute(self, player):
		player.setDirection(LEFT)
		return player.getChampion().move(LEFT)

class commandMoveRight(Command):
	def execute(self, player):
		player.setDirection(RIGHT)
		return player.getChampion().move(RIGHT)

class inputHandler:
	def __init__(self,player, buttons):
		self.buttons	= buttons
		self.player		= player
		self.ButtonA	= commandJump()
		self.ButtonB	= commandMoveLeft()
		self.ButtonC	= commandMoveRight()
		self.ButtonD	= commandAttack()

	def handle(self, keys):
		result = self.player.getChampion().onStand()
		self.player.setDirection(STAND)
		if keys[self.buttons[0]]==1:
			self.ButtonA.execute(self.player)
		if keys[self.buttons[1]]==1:
			result = self.ButtonB.execute(self.player)
		if keys[self.buttons[2]]==1:
			result = self.ButtonC.execute(self.player)
		if keys[self.buttons[3]]==1:
			result = self.ButtonD.execute(self.player)
		return result

class Player(metaclass=Singleton):
	def __init__(self, name="Player1", champion=None):
		self._name			= name
		self._direction		= 0
		self._render		= None
		self._champion		= champion
		self._rival			= None
		self._buttons		= [K_UP,K_LEFT,K_RIGHT,K_SPACE]
		self._input_handler	= inputHandler(self,self._buttons)

	def setName(self, name):
		self._name = name

	def setChampion(self, champion):
		if self._champion is None:
			self._champion = champion

	def getChampion(self):
		return self._champion

	def setRival(self, rival):
		self._rival = rival

	def getRival(self):
		return self._rival

	def setDirection(self,direction):
		self._direction = direction

	def update(self,keystate=None):
		if keystate is not None:
			self._render = self._input_handler.handle(keystate)
		else:
			if self._direction == 0:
				self._render = self._champion.onStand()
			else:
				self._render = self._champion.move(self._direction)

			self._render = self._champion.onAttack()
			self._render = self._champion.onHit()
			self._render = self._champion.onDie()
		return self._render
