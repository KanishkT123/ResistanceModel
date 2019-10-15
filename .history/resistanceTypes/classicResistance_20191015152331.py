from player import player

class classicResistance(player):
    """Classic Resistance Member
    Tries to make fair assumptions about others
    Is only capable of voting yes (As are all resistance)
    Picks highest trust players to go on missions
    Breaks ties randomly
    """
    def __init__(self, playerCount):
        super().__init__(playerCount)
        playerTrust = [0.0 for x in range(self.playerCount)]
    
    def play(self):
        """Public Method: The resistance player goes on a mission
        Resistance players can only succeed missions """
        return True
    
    def choose(self, n):
        """Public Method: 
        Input: Int n <= playerCount
        Output: List of chosenPlayers
        The resistance player attempts to choose
        a team of n players to go on a mission
        """
