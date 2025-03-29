# from config import START_COL, START_ROW, VISIBILITY, GRID_ROWS
import config
from world_elements.agent import Agent
from policy import Policy
from world_elements.world_element_encoding import ObjectType
import numpy as np
from actions import Action
from copy import deepcopy

class Simulation:
    def __init__(self, policy, worldMap):
        self.worldMap = worldMap
        self.cnt = 0
        self.agent = Agent(config.START_ROW, config.START_COL, policy, worldMap)
        self.nextState = None
        self.currState = None
        self.reward = 0
        self.action = None
    def update(self): # step procedure
        # initialize S
        self.currState = self.scrapeState() if self.cnt == 0 else self.nextState
        if self.cnt == 0:
            self.agent.policy.actions = self.worldMap.getAvailableActions(self.currState, self.agent)
        # choose A from S using Q
        self.action = self.agent.analize(self.currState)
        #take action A
        self.agent.move(self.action)
        # observe R, S'
        self.reward = self.agent.reward(Action.fromTuple(self.action))
        self.nextState = self.scrapeState()
        self.agent.policy.prevActions = self.agent.policy.actions
        self.agent.policy.updateActions(self.worldMap, self.nextState, self.agent) 
        self.agent.policy.updateQ(self.currState, self.nextState, self.reward, deepcopy(self.action), self.agent, self.worldMap.goal)
        # update cannonballs
        for row in range (config.GRID_ROWS - 1, -1, -1):
            for cannonball in self.worldMap.cannonballs[row]:
                cannonball.update()
            self.worldMap.cannonballs[row].clear()
        # fire cannons
        for cannon in self.worldMap.cannons:
            if self.cnt % cannon.rate == 0:
                cannon.fire()
        self.cnt += 1
        if self.cnt >= config.GRID_ROWS**2:
            self.agent.policy.updateQ(self.currState, self.nextState, -10, deepcopy(self.action), self.agent, self.worldMap.goal)
            return -float('inf')
        return self.reward
    
    def scrapeState(self): # surroundings of agent
        delta = (config.VISIBILITY - 1)//2
        state = np.zeros((config.VISIBILITY, config.VISIBILITY, 4), dtype=np.int32)
        for i in range (self.agent.row - delta, self.agent.row + delta + 1):
            for j in range (self.agent.col - delta, self.agent.col + delta + 1):
                rowTrans, colTrans = self.agent.row - delta, self.agent.col - delta
                for dim in range (4):
                    if ObjectType.decode(dim) == "CANNONBALL": # not only presence but also type of cannonball (step) is marked in state matrix
                        cannonball = self.worldMap.world[(i,j)][ObjectType.decode(dim)]
                        if cannonball is not None:
                            state[i - rowTrans,j - colTrans,dim] = cannonball.cannon.step
                        else:
                            state[i - rowTrans,j - colTrans,dim] = 0
                    elif ObjectType.decode(dim) == "APPLE":
                        apple = self.worldMap.world[(i,j)][ObjectType.decode(dim)]
                        if apple is not None:
                            state[i - rowTrans,j - colTrans, dim] = apple.type # type of apple is also important
                        else:
                            state[i - rowTrans,j - colTrans, dim] = 0
                    else:
                        state[i- rowTrans,j - colTrans, dim] = 0 if self.worldMap.world[(i,j)][ObjectType.decode(dim)] is None else 1
        return state