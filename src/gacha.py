import random
from prize import Prize

class GachaSystem:
    def __init__(self):
        self.prizes = [
            Prize("Sticker", "Common", 10),
            Prize("Keychain", "Rare", 50),
            Prize("Figure", "Legendary", 200)
        ]

    def roll(self):
        return random.choice(self.prizes)
