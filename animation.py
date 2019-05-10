from enum import Enum
from dataclasses import dataclass

import os
import typing

import pygame


class LoopType(Enum):
    NO_LOOP = 0
    BACK_TO_BEGINNING = 1
    REVERSE_DIRECTION = 2


@dataclass
class LoopState:
    type: LoopType = LoopType.NO_LOOP
    """Defines the type of the loop"""

    iterations: int = 0
    """Defines the number of iterations an animation loops for. if 0, loops infinitely."""


@dataclass
class Section:
    frames: typing.Tuple[pygame.Surface, ...]
    """Represents the frames for the animation"""

    direction: bool = True
    """Represents weather the animation is playing forwards or backwards; True for forwards, False for backwards"""

    loop_state: LoopState = LoopState()
    """Represent the state of the loop"""

    @classmethod
    def from_directory(cls, path: str):
        for files in os.walk(path):
            return cls(tuple(pygame.image.load(os.path.join(path, file)) for file in files[2]))


@dataclass
class Animation:
    sections: typing.List[Section]
    """Represents the sections for the animation"""

    loop_state: LoopState = LoopState()
    """Represent the state of the loop"""

    @classmethod
    def from_directory(cls, path: str):
        for files in os.walk(path):
            return cls([Section.from_directory(os.path.join(path, directory)) for directory in files[1]])
