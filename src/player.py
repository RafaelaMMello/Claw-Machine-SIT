class Player:
    def __init__(self, name):
        self.name = name
        
    def pull_gacha(self, gacha_system):
        return gacha_system.roll()
    
    