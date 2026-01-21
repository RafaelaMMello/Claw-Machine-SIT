from guest import Guest
from gacha import GachaSystem
from data_manager import DataManager

class Game:
    def __init__(self):
        self.gacha = GachaSystem()
        self.data_manager = DataManager()
        self.player = None

    def play_as_guest(self):
        self.player = Guest()

    def play_gacha(self):
        prize = self.player.play_gacha(self.gacha)
        print("You got:", prize)
