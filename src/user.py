from player import Player
from inventory import Inventory

class User(Player):
    
    def __init__(self, name, points=0):
        super().__init__(name)
        self.name = name
        self.points = points
        self.inventory = Inventory()
    
    def receive_prize(self, prize):
        self.inventory.add_item(prize)
        self.points += prize.points
    
    