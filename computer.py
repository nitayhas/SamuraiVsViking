from singleton import Singleton
from pygame.locals import *
import random

HIT_CHANCES	= 90 # x out of 100 percentage

class Computer(metaclass=Singleton):
	def __init__(self, champion, name="Computer1"):
		self.__name		= name
		self.__direction	= 0
		self.__render	= None
		self.__champion	= champion
		self.__rival		= None

	def setName(self, name):
		self.__name = name

	def setChampion(self, champion):
		if self.__champion is None:
			self.__champion = champion

	def getChampion(self):
		return self.__champion

	def setRival(self, rival):
		self.__rival = rival

	def update(self, update=True):
		if self.__rival.isAlive():
			rand = random.randint(0,100)
			if self.__champion.checkRadius(self.__rival.getRect()):
				if rand<=HIT_CHANCES:
					self.__rival._onHit(self.__champion._tryAttack())
				else:
					self.__champion._tryAttack()
			if self.__rival.getRect().left < self.getChampion().getRect().left:
				rand2 = 1
			elif self.__rival.getRect().left > self.getChampion().getRect().left:
				rand2 = 2
			else:
				rand2 = 0

			if rand<=10 and update:
				if rand2 == 1:
					self.__direction = -1
					self.__render = self.__champion._tryMove(self.__direction)
				elif rand2 == 2:
					self.__direction = 1
					self.__render = self.__champion._tryMove(self.__direction)
				else:
					self.__direction = 0
					self.__render = self.__champion._onStand()
			else:
				if self.__direction == 0:
					self.__render = self.__champion._onStand()
				else:
					self.__render = self.__champion._tryMove(self.__direction)

				self.__render = self.__champion._onAttack()
				self.__render = self.__champion._onHit()
				self.__render = self.__champion._onDie()
		else:
			self.__render = self.__champion._onStand()
		return self.__render
