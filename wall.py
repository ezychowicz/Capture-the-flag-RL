from world_element import WorldElement
class Wall(WorldElement):
    def __init__(self, row, col, worldMap):
        super().__init__(row, col, worldMap)