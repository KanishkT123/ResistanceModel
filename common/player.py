from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def __init__(self, myID, playerIDList):
        self.ID = myID
        self.playerIDList = playerIDList
    
    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def chooseMission(self):
        pass