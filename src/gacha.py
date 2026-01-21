import random
from prize import Prize

class GachaSystem:
    def __init__(self):
        self.prizes = Prize.get_all_prizes()

        self.rarity_weights = {
            "Common": 60,
            "Rare": 30,
            "Super rare": 8,
            "Legendary": 2
        }

    def roll(self):
        
        rarities = list(self.rarity_weights.keys())
        weights = list(self.rarity_weights.values())

        chosen_rarity = random.choices(rarities, weights=weights, k=1)[0]
        
        possible_prizes = [
            prize for prize in self.prizes
            if prize.rarity == chosen_rarity
        ]

        
        return random.choice(possible_prizes)