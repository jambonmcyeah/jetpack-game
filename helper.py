import os
import typing

import pygame


def load_images(path: str) -> typing.Generator[typing.Generator[pygame.Surface, None, None], None, None]:
    for files in os.walk(path):
        yield (
            pygame.image.load(os.path.join(path, file))
            for file in sorted(files[2])
        )
