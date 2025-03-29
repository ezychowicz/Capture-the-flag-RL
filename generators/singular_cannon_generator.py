from .map_generator import MapGenerator
import random
from map import Map
from .peaceful_generator import PeacefulGenerator

random.seed(111)
class SingularCannon(MapGenerator):
    def __init__(self, gridRows = random.randint(3,20), gridCols = random.randint(2,20)):
        self.gridRows = gridRows
        self.gridCols = gridCols
        
    def generateMap(self):
        peaceful = PeacefulGenerator(self.gridRows, self.gridCols)
        peacefulMap = peaceful.generateMap()
        peacefulMap.addCannon(random.randint(2,self.gridRows - 1), random.randint(1,5), random.randint(0, self.gridCols - 1))
        return peacefulMap