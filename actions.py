from enum import Enum

class Action(Enum):
    UP = (-1,0)
    DOWN = (1,0)
    LEFT = (0,-1)
    RIGHT = (0,1)
    STAY = (0,0)
    UPRIGHT = (-1,1)
    UPLEFT = (-1,-1)
    DOWNRIGHT = (1,1)
    DOWNLEFT = (1,-1)


    @staticmethod
    def fromTuple(tup):
        for action in Action:
            if action.value == tup:
                return action
        raise ValueError(f"No action found for tuple {tup}")    