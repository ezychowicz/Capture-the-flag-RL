from .map_generator import MapGenerator
import random
from map import Map
from actions import Action

# random.seed(1011)

class PeacefulGenerator(MapGenerator):
    def __init__(self, gridRows = random.randint(3,20), gridCols = random.randint(2,20)):
        self.gridRows = gridRows
        self.gridCols = gridCols
        
    def generateMap(self):
        gameMap = Map(self.gridRows, self.gridCols)
        wallsCnt = random.randint(1, self.gridRows)
        wallsPos = [(random.randint(2, self.gridRows - 1), random.randint(0, self.gridCols - 1)) for _ in range (wallsCnt)]
        goalPos = (1, random.randint(0,self.gridCols - 1))

        for row,col in wallsPos:
            gameMap.addWall(row,col)
        gameMap.addGoals([goalPos])
        return gameMap


