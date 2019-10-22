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

    @abstractmethod
    def vote(self, playersGoing):
        pass

    @abstractmethod
    def consumeResult(self, playersGoing, successes, outcome):
        pass

    @abstractmethod
    def reveal(self):
        pass