from abc import ABC, abstractmethod

class Player(ABC):
    
    @abstractmethod
    def __init__(self, playerCount):
        self.playerCount = playerCount
    
    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def chooseMission(self):
        pass