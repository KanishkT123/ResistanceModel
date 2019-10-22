from common import Player
from random import random

class classicResistance(Player):
    """Classic Resistance Member
    Tries to make fair assumptions about others
    Is only capable of voting yes (As are all resistance)
    Picks highest trust players to go on missions
    Breaks ties randomly
    """
    def __init__(self, myID, playerIDList):
        super().__init__(myID, playerIDList)
        
        #Resistance Player only trusts themselves at the start
        self.playerTrust = {ID:0.0 for ID in playerIDList}
        self.playerTrust[myID] = 100.0

        #Randomize how much each new mission changes trust criteria
        self.alpha = random()

    def play(self):
        """Public Method: The resistance player goes on a mission
        Resistance players can only succeed missions """
        return True
    
    def reveal(self):
        """Public Method: The resistance player reveals their role"""
        return True

    def chooseMission(self, n):
        """Public Method: 
        Input: Int n <= playerCount
        Output: List of chosenPlayers
        The resistance player attempts to choose
        a team of n players to go on a mission
        """
        #Sort the defaultDict according to descending trust
        finalList = sorted(self.playerTrust.items(), 
                           key=lambda k_v:k_v[1],
                           reverse = True)
        return finalList[:n]

    def __updateTrust(self, playersGoing, success, outcome):
        """Public Method:
        Inputs: playersGoing is a list of the players on the mission
        Success is a bool reflecting whether the mission was successful
        Output: null
        The resistance player updates their trust indices after a mission"""
        #Always trust yourself: Remove yourself from trust pool
        try:
            otherPlayers = playersGoing.remove(self.ID)
        except:
            otherPlayers = playersGoing

        outcomeScore = 0.0
        if success:
            outcomeScore = 100.0
        else:
            outcomeScore = -100.0
        
        perPlayerMagnitude = outcomeScore/len(otherPlayers)

        for player in otherPlayers:
            oldTrust = self.playerTrust[player]
            newTrust = self.alpha*perPlayerMagnitude + oldTrust
            
            #Edge cases handled
            #Failed 2P Mission including me: The other is a spy
            if perPlayerMagnitude == -100:
                newTrust = -100
            #Previously decided the player is a Spy
            if oldTrust <= -100:
                newTrust = oldTrust
            
            self.playerTrust[player] = newTrust
    
    def consumeResult(self, playersGoing, successes, outcome):
        __updateTrust(self, playersGoing, successes, outcome)
    
