from .champion import Champion
import copy

SAMURAI_PATH    = "Champions/images/Samurai/"
SPEED           = 7
ATTACK_SPEED    = 1
VELOCITY        = 8
MASS            = 1.8
POWER           = 5
RANGE           = 70
SHIELD          = 5
HEALTH          = 140

class Samurai(Champion):
    def __init__(self, posrect, ground):
        Champion.__init__(self,posrect,SAMURAI_PATH,ground,SPEED,ATTACK_SPEED,VELOCITY,MASS,POWER,RANGE,SHIELD,HEALTH)

    def setWeapon(self, weapon):
        if weapon.checkChampion(self._type()):
            if self._weapon is not None:
                if weapon.getHigh() > self._weapon.getHigh():
                    self._weapon = copy.deepcopy(weapon)
                    return True
            else:
                self._weapon = copy.deepcopy(weapon)
                return True
        return False
