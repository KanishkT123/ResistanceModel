from player import player
class classicResistance(player):
    """Classic Resistance Member
    Tries to make fair assumptions about others
    Is only capable of voting yes (As are all resistance)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)