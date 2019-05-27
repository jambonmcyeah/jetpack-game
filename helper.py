import os
import random
import typing

import pygame

T = typing.TypeVar("T")


def load_images(path: str) -> typing.Generator[typing.Generator[pygame.Surface, None, None], None, None]:
    for files in os.walk(path):
        files[1].sort()
        if files[2]:
            yield (
                pygame.image.load(os.path.join(files[0], file))
                for file in sorted(files[2])
            )


def chance(likelihood):
    return random.random() < likelihood


def flatten(array: typing.Union[typing.Iterable[T], T]) -> typing.Generator[T, None, None]:
    if isinstance(array, typing.Iterable):
        for value in array:
            for inner_value in flatten(value):
                yield inner_value
    else:
        yield array


def default_font(size, bold=False, italic=False):
    return pygame.font.SysFont(pygame.font.get_default_font(), size, bold, italic)
