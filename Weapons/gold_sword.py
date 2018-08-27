from .weapon import Weapon

SWORD_PATH  = "Weapons/images/gold_sword.png"
NAME        = "Gold Sword"
class Goldsword(Weapon):
    """docstring for Sword."""
    def __init__(self, low, high, whitelist):
        Weapon.__init__(self, NAME, SWORD_PATH, low, high, whitelist)
