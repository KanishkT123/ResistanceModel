from random import sample
from resistance.classicResistance import classicResistance
from spy.simpleSpy import simpleSpy

SPIES = [2,2,3,3,3,4]

class Mission:
    """Simple object for holding mission data"""
    def __init__(self, playersNeeded, successes, failsNeeded):
        self.playersNeeded = playersNeeded
        self.successes = successes
        self.failsNeeded = failsNeeded
        self.outcome = False
        self.playersGoing = []
    
class GameRunner:
    """The game runner class for Resistance
    Generates all the initial values and actually runs the game"""
    def __init__(self, playerCount):
        #Public members

        #Mission and game structure related
        self.missions = []
        self.missionCount = 0
        self.voteFail = 0
        self.offset = 0
        self.missionSuccess = 0
        self.missionFail = 0
        
        #Player related
        self.playerCount = playerCount
        self.spyCount = 0
        self.resistanceCount = 0
        self.playerIDs= []
        
        #Private members
        self.__spies = []
        self.__resistance = []
        self.__playerDict = {}

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
        """Private Method: Generates and stores players and their ID's
        Players are assigned ID's randomly to prevent training issues later
        TODO: Add arguments for specific possible spy and resistance types"""
        self.spyCount = SPIES[self.playerCount - 5]
        self.resistanceCount = self.playerCount - self.spyCount

        IDs = sample(range(0,10), self.playerCount)
        self.playerIDs = IDs
        playerDict = {}
        
        #Assign random ID's to spies and resistance
        for i in range(self.playerCount):
            if i >= resistanceCount:
                newSpy = simpleSpy(IDs[i], IDs)
                playerDict[IDs[i]] = newSpy
                self.__spies.append(IDs[i])
            else: 
                newResistance = classicResistance(IDs[i], IDs)
                playerDict[IDs[i]] = newResistance
                self.__resistance.append(newResistance)
        
        self.__playerDict = playerDict
        
        #The spies know each other and have perfect knowledge
        for id in self.__spies:
            self.__playerDict[id].spyReveal(self.__spies)
    
    def playRound(self):
        """Public method:
        Starts the next round of the game. Automatically chooses
        the captain, and calls on the captain to choose the players. 
        Makes the players play success or failures, and reveals the result."""
        #Move around in a circle to get to the next captain
        captainID = self.playerIDs[self.missionCount + self.offset % 
                                                    self.playerCount]
        captain = self.__playerDict[captainID]
        
        #Decide the mission and it's particulars
        mission = self.missions[missionCount]
        missionPlayerIDs = captain.chooseMission(mission.playersNeeded)
        #TODO: Voting functionality
        
        mission.playersGoing = missionPlayerIDs
        missionPlayers = [self.__playerDict[ID] for ID in missionPlayerIDs]
        
        #Gather player votes
        votes = []
        for player in missionPlayers:
            votes.append(player.play)

        #Figure out if the mission succeeded and update variables
        successes = sum(votes)
        mission.successes = successes

        if mission.failsNeeded <= mission.playersNeeded - successes:
            outcome = False
            self.missionFail += 1
        else:
            outcome = True
            self.missionSuccess += 1

        mission.outcome = outcome
        
        #Results given to each player
        for ID in self.__playerDict:
            self.__playerDict[ID].consumeResult(mission.playersNeeded,
                                                successes,
                                                outcome)
        
        self.missionCount += 1