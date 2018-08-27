from singleton import Singleton
from pygame.locals import *
import random

HIT_CHANCES	= 90 # x out of 100 percentage

class Computer(metaclass=Singleton):
	def __init__(self, name="Computer1", champion=None):
		self._name		= name
		self._direction	= 0
		self._render	= None
		self._champion	= champion
		self._rival		= None

	def setName(self, name):
		self._name = name

	def setChampion(self, champion):
		if self._champion is None:
			self._champion = champion

	def getChampion(self):
		return self._champion

	def setRival(self, rival):
		self._rival = rival

	def update(self, update=True):
		if self._rival.isAlive():
			rand = random.randint(0,100)
			if self._champion.checkRadius(self._rival.getRect()):
				if rand<=HIT_CHANCES:
					self._rival.onHit(self._champion.attack())
				else:
					self._champion.attack()
			if self._rival.getRect().left < self.getChampion().getRect().left:
				rand2 = 1
			elif self._rival.getRect().left > self.getChampion().getRect().left:
				rand2 = 2
			else:
				rand2 = 0

			if rand<=10 and update:
				if rand2 == 1:
					self._direction = -1
					self._render = self._champion.move(self._direction)
				elif rand2 == 2:
					self._direction = 1
					self._render = self._champion.move(self._direction)
				else:
					self._direction = 0
					self._render = self._champion.onStand()
			else:
				if self._direction == 0:
					self._render = self._champion.onStand()
				else:
					self._render = self._champion.move(self._direction)

				self._render = self._champion.onAttack()
				self._render = self._champion.onHit()
				self._render = self._champion.onDie()
		else:
			self._render = self._champion.onStand()
		return self._render
