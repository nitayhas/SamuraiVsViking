import pygame
from pygame.locals import *
import random
import copy

class Weapon(object):
    """docstring for Weapon."""
    def __init__(self, name, image_path, low, high, champions_whitelist):
        self._name          = name
        self._image_path    = image_path
        self._low           = low
        self._high          = high
        self._whitelist     = champions_whitelist
        self._rect          = None

    def getWeaponPower(self):
            return random.randint(self._low,self._high)

    def checkChampion(self, champion_type):
        if champion_type in self._whitelist:
            return True
        return False

    def setPosition(self,rect):
        self._rect = copy.deepcopy(rect)

    def getPosition(self):
        return self._rect

    def update(self):
        image = pygame.image.load(self._image_path).convert_alpha()
        try:
            image = pygame.transform.scale(image, self._rect.size)
            image = image.convert_alpha()
        except Exception as exp:
            print("EXP")
        return (image,self._rect)
