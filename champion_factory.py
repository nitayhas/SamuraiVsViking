######
# Factory design pattern for champions
####
from Champions import *

class ChampionFactory:
    def create_champion(self, champion_type, position_rect, ground):
        targetclass = champion_type.capitalize()
        if targetclass in globals():
            return globals()[targetclass](position_rect, ground)
        return None
