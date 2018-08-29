from singleton import Singleton
from ComputerStrategies import *
from pygame.locals import *

HIT_CHANCES	= 90 # x out of 100 percentage

class Computer(metaclass=Singleton):
	def __init__(self, champion, name="Computer1", strategy=ComputerStrategyA(), hit_changes=HIT_CHANCES):
		self.__name			= name
		self.__direction	= 0
		self.__render		= None
		self.__champion		= champion
		self.__rival		= None
		self.__strategy 	= strategy
		self.__hit_chances	= hit_changes

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

	def setDirection(self, direction):
		self.__direction = direction

	def getDirection(self):
		return self.__direction

	def setHitChanges(self, hit_chances):
		self.__hit_chances = hit_chances

	def getHitChanges(self):
		return self.__hit_chances

	def getRender(self):
		return self.__render

	def update(self):
		self.__render = self.__strategy.algorithm_execution(self)
		return self.__render
