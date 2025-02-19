from world_element import WorldElement
# from config import DEATH_REWARD, GOAL_REWARD, APPLE1_REWARD, APPLE2_REWARD, STAGNATION_REWARD, NOTHING_REWARD, GRID_ROWS
import config
from actions import Action
from pathlib import Path
from config import load_image, CELL_SIZE
class Agent(WorldElement):
    def __init__(self, row, col, policy, worldMap):
        super().__init__(row, col, worldMap)
        self.policy = policy
        
    def analize(self, state):
        actions = self.worldMap.getAvailableActions(state, self)
        action = self.policy.chooseAction(state, self, actions, self.worldMap.goal)
        return action
    
    def move(self, action):
        self.row += action[0]
        self.col += action[1]
        

    def reward(self, takenAction): 
        # bonus for higher row:
        bonus = (config.GRID_ROWS - self.row)*0.1
        if self.worldMap.world[(self.row, self.col)]["CANNONBALL"] is not None:
            return config.DEATH_REWARD
        elif self.worldMap.world[(self.row, self.col)]["GOAL"] is not None:
            return config.GOAL_REWARD
        elif self.worldMap.world[(self.row, self.col)]["APPLE"] is not None:
            if self.worldMap.world[(self.row, self.col)]["APPLE"].type == 1:
                self.worldMap.world[(self.row, self.col)]["APPLE"] = None
                return config.APPLE1_REWARD + bonus
            else:
                self.worldMap.world[(self.row, self.col)]["APPLE"] = None
                return config.APPLE2_REWARD + bonus
            
        if takenAction == Action.STAY:
            return config.STAGNATION_REWARD + bonus
        return config.NOTHING_REWARD + bonus
    
    def flagCaptured(self):
        return self.worldMap.world[(self.row, self.col)]["GOAL"] is not None
    
    def isDead(self):
        return self.worldMap.world[(self.row, self.col)]["CANNONBALL"] is not None
            
    def drawAgent(self, screen):
        screen.blit(load_image(Path("assets")/"agent.png"), (CELL_SIZE*self.col, CELL_SIZE*self.row))