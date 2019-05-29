""" Author: Jun Bo Bi
    Date: May 29, 2019
    Desc: Animations
"""

import enum

import os
import copy
import typing

import pygame

SPEED: int = 4

T = typing.TypeVar("T")


class LoopType(enum.IntEnum):
    """A class representing loop types"""

    BACK_TO_OTHER_END = 1
    REVERSE_DIRECTION = 2
    REPEAT_LAST_FRAME = 3


class LoopState:
    """Initializer for the LoopState class"""

    def __init__(self, loop_type=LoopType.BACK_TO_OTHER_END, iterations=1, direction=True):
        """Initializer for the LoopState class"""
        self.loop_type = loop_type
        self.iterations = iterations
        self.direction = direction


class Loopable(typing.Iterable[T]):
    """
    Represents a loopable class, inherits from Iterable,
    """

    def __init__(self, loop_state: typing.Optional[LoopState] = None):
        if loop_state is None:
            loop_state = LoopState()

        self.loop_state = loop_state

    @property
    def array(self) -> typing.Union[typing.List[T], typing.Tuple[T, ...]]:
        """Getter for the array attribute of this Loopable"""
        raise NotImplementedError

    @property
    def loop_state(self) -> LoopState:
        """Getter for the loop_state attribute of this Loopable"""
        return self.__loop_state

    @loop_state.setter
    def loop_state(self, value: loop_state):
        """Setter for the loop_state attribute of this Loopable"""
        self.__loop_state = value

    def __iter__(self):
        """__iter__ method for this Loopable"""
        return LoopableIter[T](self)


class LoopableIter(typing.Iterator[T]):
    """Iterator for the loopable class"""

    def __init__(self, loopable: Loopable[T], loop_state: typing.Optional[LoopState] = None,
                 current_item: typing.Optional[int] = None):
        """Initializer for the LoopableIter class"""

        if loop_state is None:
            loop_state = copy.deepcopy(loopable.loop_state)

        if current_item is None:
            current_item = 0 if loop_state.direction else len(loopable.array) - 1

        self.__loopable: Loopable = loopable
        self.__loop_state: LoopState = loop_state
        self.__current_item: int = current_item

    @property
    def current_item(self) -> int:
        """Getter for the current_item attribute of this LoopableIter"""
        return self.__current_item

    @property
    def loop_state(self) -> LoopState:
        """Getter for the loop_state attribute of this LoopableIter"""
        return self.__loop_state

    @property
    def loopable(self) -> Loopable:
        """Getter for the loopable attribute of this LoopableIter"""
        return self.__loopable

    def __next__(self) -> T:
        """__next__ method for this LoopableIter"""

        # If the end of the array is reached
        if self.__current_item >= len(self.__loopable.array) or self.__current_item < 0:
            if self.loop_state.iterations > 0:
                self.loop_state.iterations -= 1

            if self.loop_state.iterations == 0:
                raise StopIteration

            if self.__loop_state.loop_type == LoopType.REVERSE_DIRECTION:
                self.__loop_state.direction = not self.__loop_state.direction

                if self.__loop_state.direction:
                    self.__current_item += 2
                else:
                    self.__current_item -= 2

            elif self.__loop_state.loop_type == LoopType.BACK_TO_OTHER_END:
                if self.__current_item < 0:
                    self.__current_item = len(self.__loopable.array) - 1
                else:
                    self.__current_item = 0

            elif self.__loop_state.loop_type == LoopType.REPEAT_LAST_FRAME:
                if not self.__loop_state.direction:
                    self.__current_item += 1
                else:
                    self.__current_item -= 1

                return self.__loopable.array[self.__current_item]

        current_item = self.__loopable.array[self.__current_item]

        if self.__loop_state.direction:
            self.__current_item += 1
        else:
            self.__current_item -= 1

        return current_item


class Section(Loopable[pygame.Surface]):
    """A class representing sections, inherits from Loopable"""
    def __init__(self, frames: typing.Tuple[pygame.Surface, ...], loop_state: typing.Optional[LoopState] = None):
        if loop_state is None:
            loop_state = LoopState()

        super().__init__(loop_state)

        self.__frames = frames

    @classmethod
    def from_directory(cls, path: str, loop_state: typing.Optional[LoopState] = None):
        """Loads a section from a directory"""
        if loop_state is None:
            loop_state = LoopState()

        for files in os.walk(path):
            return cls(
                tuple(
                    pygame.image.load(os.path.join(files[0], file))
                    for file in sorted(files[2])
                ),
                loop_state
            )

    @property
    def frames(self) -> typing.Tuple[pygame.Surface, ...]:
        """Getter for the frames attribute of this Section"""
        return self.__frames

    @property
    def array(self) -> typing.Tuple[pygame.Surface, ...]:
        """Getter for the array attribute of this Section"""
        return self.frames


class Animation(Loopable[Section]):
    """A class representing animations, inherits from Loopable"""
    def __init__(self, sections: typing.List[Section], loop_state: typing.Optional[LoopState] = None):
        """Initializer for the Animation class"""
        if loop_state is None:
            loop_state = LoopState()

        super().__init__(loop_state)

        self.sections = sections

    @property
    def array(self) -> list:
        """Getter for the array attribute of this Animation"""
        return self.sections

    @classmethod
    def from_directory(cls, path: str,
                       loop_state: typing.Optional[LoopState] = None,
                       section_loopstates: typing.Optional[typing.List[LoopState]] = None):
        """Loads a animation from a directory"""

        for files in os.walk(path):
            if section_loopstates is None:
                section_loopstates = [LoopState() for _ in range(len(files[1]))]

            return cls(
                [
                    Section.from_directory(os.path.join(files[0], directory), section_loopstate)
                    for directory, section_loopstate in zip(sorted(files[1]), section_loopstates)
                ],
                loop_state
            )
