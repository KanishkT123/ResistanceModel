class Mission:
    """Simple object for holding mission data"""
    def __init__(self, takingPart, successes):
        self.takingPart = takingPart
        self.successes = successes
    
class GameRunner:
    """The game runner class for Resistance
    Generates all the initial values and actually runs the game"""
    def __init__(self, players):
        self.missions = []
        self.missionCount = 0
        self.missionSuccess = 0
        self.missionFail = 0
        self.voteFail = 0

        self.spies = []
        self.resistance = []

        if players < 5 or players > 10:
            Ex = ValueError()
            Ex.strerror = "Player value must be within 5 and 10, inclusive"
            raise Ex
        
        self.players = players
        self.__missionGenerator()

        
    
    def __missionGenerator(players):
        """Generates missions for the gameRunner using number of players"""
        