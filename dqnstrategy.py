import torch
import torch.nn as nn
import torch.optim as optim
import random
from collections import deque
import numpy as np
from policy import Policy
from dqn import DQN
from actions import Action
class DQNStrategy(Policy):
    """
    Deep Qlearning. Still uses Qlearning, but doesnt store Q function in a matrix. Instead of it, it uses neural network.
    """
    def __init__(self, stateSize, actionSize, gamma=0.9, lr=0.001):
        self.stateSize = stateSize
        self.actionSize = actionSize # for impossible actions -inf
        self.gamma = gamma  # discount
        self.alpha = 0.1  # exploration
        self.memory = deque(maxlen=2000)  

        # model
        self.model = DQN(stateSize, actionSize)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr) # adam optimizer
        self.lossFn = nn.MSELoss() # mean squared error loss function

    @staticmethod
    def prepareState(state, agent, takenAction = (0,0)): # in this method it will flatten the 3-dim matrix and concatenate the agent position. loss of spacial info
        state = state.flatten()
        state = np.concatenate(([agent.row - takenAction[0], agent.col - takenAction[1]], state))
        return torch.FloatTensor(state)
    
    def updateQ(self, prevState, nextState, reward, takenAction, agent):
        prevState = DQNStrategy.prepareState(prevState, agent, takenAction).unsqueeze(0) # add necessary info to a tensor
        nextState = DQNStrategy.prepareState(nextState, agent).unsqueeze(0)

        target = reward
        target += self.gamma * torch.max(self.model(nextState)).item()

        predictedQ = self.model(prevState)[0, takenAction]  # returns a vector of predicted Q(s,_) by nn

        loss = self.lossFn(predictedQ, torch.tensor(target)) # predicted Q vs actual reward
        self.optimizer.zero_grad() # reset
        loss.backward()  # calculate gradient for weights
        self.optimizer.step()  # update weights in nn

    def chooseAction(self, state, agent, actions):
        if np.random.rand() < self.alpha:  # explore
            return random.choice(actions)
        state = DQNStrategy.prepareState(state, agent).unsqueeze(0)
        with torch.no_grad():
            nnOutput = self.model(state).squeeze(0) # unpack output to Q(s,_) vector
            allActions = [action.value for action in list(Action)]
            mask = torch.tensor([action in actions for action in allActions], dtype=torch.bool, device=nnOutput.device)
            nnOutput[~mask] = -float('inf') # if action not in actions then -float(inf)
            return allActions[torch.argmax(nnOutput).item()] # item rozpakowuje z tensora