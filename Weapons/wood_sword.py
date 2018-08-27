from .weapon import Weapon

SWORD_PATH  = "Weapons/images/wood_sword.png"
NAME        = "Wood Sword"

class Woodsword(Weapon):
    """docstring for Sword."""
    def __init__(self, low, high, whitelist):
        Weapon.__init__(self, NAME, SWORD_PATH, low, high, whitelist)
