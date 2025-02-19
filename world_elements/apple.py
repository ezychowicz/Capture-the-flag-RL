from world_elements.world_element import WorldElement

class Apple(WorldElement):
    def __init__(self, type, row, col, worldMap):
        super().__init__(row, col, worldMap)
        self.type = type



