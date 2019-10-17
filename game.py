from random import sample
from resistance.classicResistance import classicResistance

SPIES = [2,2,3,3,3,4]

class Mission:
    """Simple object for holding mission data"""
    def __init__(self, takingPart, successes, failsNeeded):
        self.takingPart = takingPart
        self.successes = successes
        self.failsNeeded = failsNeeded
    
class GameRunner:
    """The game runner class for Resistance
    Generates all the initial values and actually runs the game"""
    def __init__(self, playerCount):
        #Public members
        self.missions = []
        self.missionCount = 0
        self.voteFail = 0
        self.playerCount = playerCount
        self.spyCount = 0
        self.resistanceCount = 0
        self.missionSuccess = 0
        self.missionFail = 0

        #Private members
        self.__spies = []
        self.__resistance = []

        if self.playerCount < 5 or self.playerCount > 10:
            Ex = ValueError()
            Ex.strerror = "Player value must be within 5 and 10, inclusive"
            raise Ex

        self.__missionGenerator()
        self.__playerGenerator()

    def __missionGenerator(self):
        """Private method:
        Generates and stores missions for the gameRunner
        using self.playerCount"""
        playerCount = self.playerCount

        if playerCount == 5:
            participating = [2,3,2,3,3]
            self.missions = [Mission(x, 0, 1) for x in participating]

        if playerCount == 6:
            participating = [2,3,4,3,4]
            self.missions = [Mission(x, 0, 1) for x in participating]

        if playerCount == 7:
            participating = [2,3,3,4,4]

        else:
            participating = [3,4,4,5,5]

        self.missions = [Mission(participating[i], 0, 1) if i <=5 
                        else Mission(participating[i],0,2) 
                        for i in range(5)]   

    def __playerGenerator(self):
        """Private Method: Generates and stores players
        TODO: Add arguments for specific possible combinations"""
        self.spyCount = SPIES[self.playerCount - 5]
        self.resistanceCount = self.playerCount - self.spyCount

        IDs = sample(range(0,10), self.playerCount)
        playerDict = {}

        for i in range(self.playerCount):
            if i >= resistanceCount:
                newSpy = Spy(IDs[i], IDs)
                playerDict[IDs[i]] = newSpy
            else: 
                newResistance = classicResistance(IDs[i], IDs)
                playerDict[IDs[i]] = newResistance