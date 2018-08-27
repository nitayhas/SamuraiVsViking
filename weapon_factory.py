######
# Factory design pattern for weapons
####
from Weapons import *

class WeaponFactory:
    def create_weapon(self, typ, low, high, whitelist):
        targetclass = typ.capitalize()
        if targetclass in globals():
            return globals()[targetclass](low, high,whitelist)
        return None
