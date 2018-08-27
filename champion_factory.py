######
# Factory design pattern for champions
####
from Champions import *

class ChampionFactory:
    def create_champion(self, typ, position_rect, ground):
        targetclass = typ.capitalize()
        if targetclass in globals():
            return globals()[targetclass](position_rect, ground)
        return None
