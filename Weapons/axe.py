from .weapon import Weapon

AXE_PATH    = "Weapons/images/axe.png"
NAME        = "Axe"

class Axe(Weapon):
    """docstring for Sword."""
    def __init__(self, low, high, whitelist):
        Weapon.__init__(self, NAME, AXE_PATH, low, high, whitelist)
