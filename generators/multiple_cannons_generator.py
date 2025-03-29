from .map_generator import MapGenerator
import random
from map import Map
from .peaceful_generator import PeacefulGenerator

random.seed(111)
class MultipleCannons(MapGenerator):
    def __init__(self, gridRows = random.randint(3,20), gridCols = random.randint(2,20)):
        self.gridRows = gridRows
        self.gridCols = gridCols
        
    def generateMap(self):
        peaceful = PeacefulGenerator(self.gridRows, self.gridCols)
        peacefulMap = peaceful.generateMap()
        cannonsNum = random.randint(1, self.gridCols)
        positions = random.sample(range(self.gridCols), cannonsNum)
        for pos in positions:
            peacefulMap.addCannon(random.randint(1,self.gridRows - 1), random.randint(1,5), pos)
        return peacefulMap