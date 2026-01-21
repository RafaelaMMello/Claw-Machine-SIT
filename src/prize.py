class Prize:
    def __init__(self, name, rarity, points):
        self.name = name
        self.rarity = rarity
        self.points = points

    def __str__(self):
        return f"{self.name} ({self.rarity}) - {self.points} pts"
