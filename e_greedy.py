import numpy as np
import random
# random.seed(10)
def egreedy(QValues, actions, epsilon):
    if np.random.rand() < epsilon:
        return random.choice(actions)
    else:
        max_Q = max([Qval for action, Qval in QValues.items() if action in actions])
        # max_Q = max(QValues.values())
        best_actions = [a for a in actions if a in QValues and QValues[a] == max_Q]
        # return random.choice(best_actions) 
        return best_actions[0]