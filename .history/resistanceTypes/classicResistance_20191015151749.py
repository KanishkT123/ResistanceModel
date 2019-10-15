from player import player

class classicResistance(player):
    """Classic Resistance Member
    Tries to make fair assumptions about others
    Is only capable of voting yes (As are all resistance)
    """
    def __init__(self, playerCount):
        super().__init__(playerCount)
        playerTrust = [0.0 for x in range(self.playerCount)]
    
    def play:(self):
        return "Success"