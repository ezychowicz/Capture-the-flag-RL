from collections import defaultdict
import numpy as np
from policy import Policy
from e_greedy import egreedy
import config
class Qlearning(Policy):
    def __init__(self):
        self.actions = []
        self.prevActions = []
        self.Q = dict()
        self.alfa = 0.1
        self.lamb = 0.9
        
    def updateQ(self, prevState, newState, reward, takenAction, agent, goal, done = False): # lambda - discounts, alpha - speed of learning
        prevState = (Qlearning.makeHashable(prevState), abs((agent.row - takenAction[0] - goal[0])) + abs((agent.col - takenAction[1] - goal[1]))) # there is a distance to goal in state (agent knows it, its like a potential field)
        newState = (Qlearning.makeHashable(newState), abs((agent.row - goal[0])) + abs((agent.col - goal[1])))
        if newState not in self.Q:
            self.Q[newState] = dict()
        for action in self.actions:
            if action not in self.Q[newState]:
                self.Q[newState][action] = 0
        
        # if takenAction not in self.Q[prevState]:
            # print("???????????", self.Q[prevState], "\nTAKEN ACTION", takenAction, "\nPREV ACTIONS",self.prevActions,"\nACTIONS:",self.actions)
        self.Q[prevState][takenAction] = self.Q[prevState][takenAction] + self.alfa*(reward + self.lamb*max(self.Q[newState].values()) - self.Q[prevState][takenAction]) 
    
    def chooseAction(self, state, agent, actions, goal): # agent is needed as his position is a part of state
        state = (Qlearning.makeHashable(state), abs((agent.row - goal[0])) + abs((agent.col - goal[1])))
        if state not in self.Q: # to sie dzieje tylko przy pierwszej iteracji
            self.Q[state] = dict()
            for action in actions:
                self.Q[state][action] = 0
        return egreedy(self.Q[state], actions, epsilon=0.1)
        
    def makeHashable(state):
        newState = []
        for matrix in state:
            newMatrix = tuple(map(lambda row: tuple(row.tolist()), matrix))
            newState.append(newMatrix)
        return tuple(newState)