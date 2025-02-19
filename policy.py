from abc import ABC, abstractmethod

class Policy(ABC):
    @abstractmethod
    def chooseAction(self, state, agent, actions, goal):
        """Decides which action to take given the state and available actions."""
        pass

    def updateActions(self, worldMap, state, agent): # available actions
        self.actions = worldMap.getAvailableActions(state, agent)