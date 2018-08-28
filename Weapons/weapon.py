import pygame
from pygame.locals import *
import random
import copy

class Weapon:
    """docstring for Weapon."""
    def __init__(self, name, image_path, low, high, champions__whitelist):
        self.__name          = name
        self.__image_path    = image_path
        self.__low           = low
        self.__high          = high
        self.__whitelist     = champions__whitelist
        self.__rect          = None

    def getLow(self):
        return self.__low

    def getHigh(self):
        return self.__high

    def getWeaponPower(self):
            return random.randint(self.__low,self.__high)

    def checkChampion(self, champion_type):
        if champion_type in self.__whitelist:
            return True
        return False

    def setPosition(self,rect):
        self.__rect = copy.deepcopy(rect)

    def getPosition(self):
        return self.__rect

    def update(self):
        image = pygame.image.load(self.__image_path).convert_alpha()
        try:
            image = pygame.transform.scale(image, self.__rect.size)
            image = image.convert_alpha()
        except Exception as exp:
            print("EXP")
        return (image,self.__rect)
