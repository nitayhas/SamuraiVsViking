######
# Factory design pattern for weapons
####
from Weapons import *

class WeaponFactory:
    def create_weapon(self, weapon_type, low, high, whitelist):
        targetclass = weapon_type.capitalize()
        if targetclass in globals():
            return globals()[targetclass](low, high,whitelist)
        return None
