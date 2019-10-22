from common import Player
from collections import defaultdict
from random import random

class simpleSpy(Player):
    """A simple Spy Class that follows the following rules:
    1. Always fail a mission if there are no other spies on it
    2. A small chance to fail the mission if there are other spies
    (Chance decided randomly)
    """
    def __init__(self, myID, playerIDList):
        super().__init__(myID, playerIDList)
        #Resistance Player only trusts themselves at the start
        self.playerTrust = defaultdict(float)
        self.playerTrust[self.ID] = 100

        #Randomize how much each new mission changes trust criteria
        self.alpha = random()
    
    def play(self):
        return super().play()
    
    def reveal(self):
        return False

    def chooseMission(self):
        return super().chooseMission()
    
    def vote(self, playersGoing):
        return super().vote(playersGoing)
    
    def consumeResult(self, playersGoing, successes, outcome):
        """Public method. However, the spies don't need to update
        their trust of other players, since they have perfect information."""
        pass

    def spyReveal(self):
        pass