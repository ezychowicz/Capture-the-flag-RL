from world_element import WorldElement
from cannonball import Cannonball
class Cannon(WorldElement):
    def __init__(self,column, rate, step, worldMap):
        super().__init__(worldMap.height, column, worldMap)
        self.rate = rate
        self.step = step
     
    def fire(self):
        newCannonball = Cannonball(self) 
        if newCannonball.isValid():
            self.worldMap.world[(self.step, self.col)]["CANNONBALL"] = newCannonball 
            self.worldMap.cannonballs[self.step].add(newCannonball)
        
