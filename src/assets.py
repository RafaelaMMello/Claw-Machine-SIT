import pygame
import os

BASE_DIR = os.path.dirname(__file__)

def load_prize_images():
    return {
        "duck": pygame.image.load(
            os.path.join(BASE_DIR, "duck.png")
        ),
        "dog": pygame.image.load(
            os.path.join(BASE_DIR, "dog.png")
        ),
        "bear": pygame.image.load(
            os.path.join(BASE_DIR, "bear.png")
        ),
        "robot": pygame.image.load(
            os.path.join(BASE_DIR, "robot.png")
        )
    }
