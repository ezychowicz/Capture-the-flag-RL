from .map_generator import MapGenerator
import random
from map import Map
from .multiple_cannons_generator import MultipleCannons


class CannonsApples(MapGenerator):
    def __init__(self, gridRows = random.randint(3,20), gridCols = random.randint(2,20)):
        self.gridRows = gridRows
        self.gridCols = gridCols
        
    def generateMap(self):
        mapGen = MultipleCannons()
        map = mapGen.generateMap()
        posRows = random.sample(range(1, self.gridRows - 1), 2)
        posCols = random.sample(range(0, self.gridCols - 1), 2)
        positions = list(zip(posRows, posCols))
        for row,col in positions:
            map.addApple(row,col,random.randint(1,2))
        return map