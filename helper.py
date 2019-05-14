import os

import pygame


def load_images(path: str):
    for files in os.walk(path):
        yield (
            pygame.image.load(os.path.join(path, file))
            for file in sorted(files[2])
        )
