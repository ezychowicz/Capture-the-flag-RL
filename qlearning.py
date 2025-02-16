from collections import defaultdict
import numpy as np
from policy import Policy
from e_greedy import egreedy

class Qlearning(Policy):
    def __init__(self):
        self.actions = []
        self.Q = defaultdict(lambda: {action: 0 for action in self.actions})
        self.alfa = 0.1
        self.lamb = 0.9

    def updateQ(self, prevState, nextState, reward, takenAction, agent, done = False): # lambda - discounts, alpha - speed of learning
        prevState = (Qlearning.makeHashable(prevState), agent.row - takenAction[0], agent.col - takenAction[1])
        newState = (Qlearning.makeHashable(nextState), agent.row, agent.col)
        self.Q[prevState][takenAction] = self.Q[prevState][takenAction] + self.alfa*(reward + self.lamb*max(self.Q[newState].values())) - self.Q[prevState][takenAction] 
    
    def chooseAction(self, state, agent, actions): # agent is needed as his position is a part of state
        state = (Qlearning.makeHashable(state), agent.row, agent.col)
        if state not in self.Q:
            for action in actions:
                self.Q[state][action] = 0
        return egreedy(self.Q[state], epsilon=0.1)
        
    def makeHashable(state):
        newState = []
        for matrix in state:
            newMatrix = tuple(map(lambda row: tuple(row.tolist()), matrix))
            newState.append(newMatrix)
        return tuple(newState)