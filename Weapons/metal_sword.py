from .weapon import Weapon

SWORD_PATH  = "Weapons/images/metal_sword.png"
NAME        = "Metal Sword"

class Metalsword(Weapon):
    """docstring for Sword."""
    def __init__(self, low, high, whitelist):
        Weapon.__init__(self, NAME, SWORD_PATH, low, high, whitelist)
