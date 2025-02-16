import numpy as np
import random
def egreedy(QValues, epsilon):
    if np.random.rand() < epsilon:
        return random.choice(list(QValues.keys()))
    else:
        max_Q = max(QValues.values())
        best_actions = [a for a, q in QValues.items() if q == max_Q]
        return random.choice(best_actions) 