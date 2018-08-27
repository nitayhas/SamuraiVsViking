from .weapon import Weapon

AXE_PATH    = "Weapons/images/double_axe.png"
NAME        = "Double Axe"
class Doubleaxe(Weapon):
    """docstring for Sword."""
    def __init__(self, low, high, whitelist):
        Weapon.__init__(self, NAME, AXE_PATH, low, high, whitelist)
