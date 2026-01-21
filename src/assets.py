import pygame
import os

BASE_DIR = os.path.dirname(__file__)

def load_prize_images():
    return {
        "duck": pygame.image.load(
            os.path.join(BASE_DIR, "duck.png")
        )
    }