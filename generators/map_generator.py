from abc import ABC, abstractmethod

class MapGenerator(ABC):
    # __init__?
    @abstractmethod
    def generateMap(self):
        '''
        Generates map with functions: addCannon, addWall etc.
        '''
        pass