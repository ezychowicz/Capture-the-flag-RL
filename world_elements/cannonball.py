from world_elements.world_element import WorldElement
# from config import GRID_ROWS
import config

class Cannonball(WorldElement):
    def __init__(self, cannon):
        super().__init__(cannon.step, cannon.col, cannon.worldMap)
        self.cannon = cannon

    def update(self): # update cannonball position
        self.worldMap.world[(self.row, self.col)]["CANNONBALL"] = None
        self.row += self.cannon.step
        if self.isValid():
            self.worldMap.world[(self.row, self.col)]["CANNONBALL"] = self
            self.worldMap.cannonballs[self.row].add(self)
    def isValid(self):
        return self.worldMap.world[(self.row, self.col)]["WALL"] is None and self.row < config.GRID_ROWS
            