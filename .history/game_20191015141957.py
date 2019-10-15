class Mission:
    """Simple object for holding mission data"""
    def __init__(self, takingPart, successes, failsNeeded):
        self.takingPart = takingPart
        self.successes = successes
        self.failsNeeded = failsNeeded
    
class GameRunner:
    """The game runner class for Resistance
    Generates all the initial values and actually runs the game"""
    def __init__(self, players):
        #Public members
        self.missions = []
        self.missionCount = 0
        self.missionSuccess = 0
        self.missionFail = 0
        self.voteFail = 0
        self.players = players

        #Private members
        self.__spies = []
        self.__resistance = []
        
        if self.players < 5 or self.players > 10:
            Ex = ValueError()
            Ex.strerror = "Player value must be within 5 and 10, inclusive"
            raise Ex
        
        self.__missionGenerator()


    def __missionGenerator(players=self.players):
        """Private method:
        Input: Int #Players
        Output: Int List of players on each mission
        Generates missions for the gameRunner using number of players"""
        if players == 5:
            return [2,3,2,3,3]
        if players == 6:
            return [2,3,4,3,4]
        if players == 7:
            return [2,3,3,4,4]
        else:
            return [3,4,4,5,5]