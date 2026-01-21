class Prize:
    def __init__(self, name, rarity, points):
        self.name = name
        self.rarity = rarity
        self.points = points

    def __str__(self):
        return f"{self.name} ({self.rarity}) - {self.points} pts"

    # LISTA ESTÁTICA DE PRÊMIOS
    PRIZES = [
        # Common
        ("duck", "Common", 25),
        ("duck", "Common", 25),

        # Rare
        ("dog", "Rare", 100),
        ("dog", "Rare", 100),

        # Super rare
        ("bear", "Super rare", 150),
        ("bear", "Super rare", 150), 
        
        # Legendary
        ("robot", "Legendary", 200),
        ("robot", "Legendary", 200)
    ]

    @staticmethod
    def get_all_prizes():
        return [Prize(name, rarity, points) for name, rarity, points in Prize.PRIZES]
