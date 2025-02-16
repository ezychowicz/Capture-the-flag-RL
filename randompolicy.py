import random
from policy import Policy

class RandomPolicy(Policy):
    def chooseAction(self, state, agent, actions):
        return random.choice(actions)
    
  