from .map_generator import MapGenerator
import random
from map import Map
from actions import Action

class PeacefulGenerator(MapGenerator):
    def __init__(self, gridRows = random.randint(3,10), gridCols = random.randint(2,10)):
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


