from .champion import Champion
import copy

VIKING_PATH     = "Champions/images/Viking/"
SPEED           = 3
ATTACK_SPEED    = 3
VELOCITY        = 5.7
MASS            = 1.8
POWER           = 8
RANGE           = 60
SHIELD          = 10
HEALTH          = 200

class Viking(Champion):
    def __init__(self, posrect, ground):
        Champion.__init__(self,posrect,VIKING_PATH,ground,SPEED,ATTACK_SPEED,VELOCITY,MASS,POWER,RANGE,SHIELD,HEALTH)

    def setWeapon(self, weapon):
        if weapon.checkChampion(self.__class__.__name__):
            if self._weapon is not None:
                if weapon._high > self._weapon._high:
                    self._weapon = copy.deepcopy(weapon)
                    return True
            else:
                self._weapon = copy.deepcopy(weapon)
                return True
        return False
