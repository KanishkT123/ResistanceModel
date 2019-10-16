from common import Player
from collections import defaultdict
class classicResistance(Player):
    """Classic Resistance Member
    Tries to make fair assumptions about others
    Is only capable of voting yes (As are all resistance)
    Picks highest trust players to go on missions
    Breaks ties randomly
    """
    def __init__(self, myID, playerIDList):
        super().__init__(myID, playerIDList)
        self.playerTrust = defaultdict(float)
        self.playerTrust[self.ID] = 100

    def play(self):
        """Public Method: The resistance player goes on a mission
        Resistance players can only succeed missions """
        return True

    def chooseMission(self, n):
        """Public Method: 
        Input: Int n <= playerCount
        Output: List of chosenPlayers
        The resistance player attempts to choose
        a team of n players to go on a mission
        """
        #Sort the defaultDict
        finalList = sorted(self.playerTrust.items(), key=lambda k_v:k_v[1][2])
        return finalList[:n]

    def updateTrust(self, missionPlayers, success):
        """Public Method:
        Inputs: missionPlayers is a list of the players on the mission
        Success is a bool reflecting whether the mission was successful
        Output: null
        The resistance player updates their trust indices after a mission"""
        #Always trust yourself 
        try:
            otherPlayers = missionPlayers.remove(self.ID)
        except:
            otherPlayers = missionPlayers
        
        
