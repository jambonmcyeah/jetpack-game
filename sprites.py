import os
import enum
import typing

import pygame

import animation


class GenericSprite(pygame.sprite.Sprite):
    """A class to represent generic sprites"""

    def __init__(self, image: pygame.Surface, position: typing.Tuple[int, int], *groups: pygame.sprite.Group, **kwargs):
        """Initializer for the GenericSprite class, sets the image and rect instance variables"""
        super().__init__(*groups)

        self.image = image
        self.position = position

    @property
    def image(self) -> pygame.Surface:
        return self.__image

    @image.setter
    def image(self, value: pygame.Surface):
        try:
            position = self.position
        except AttributeError:
            position = (0, 0)

        self.__image: pygame.Surface = value
        self.__rect: pygame.Rect = self.__image.get_rect()

        self.position = position

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @property
    def size(self) -> typing.Tuple[int, int]:
        return self.image.get_size()

    @size.setter
    def size(self, value: typing.Tuple[int, int]):
        self.image = pygame.transform.scale(self.image, value)

    @property
    def position(self) -> typing.Tuple[int, int]:
        return self.rect.left, self.rect.top

    @position.setter
    def position(self, value: typing.Tuple[int, int]):
        self.rect.left, self.rect.top = value

    @property
    def left(self) -> int:
        return self.rect.left

    @left.setter
    def left(self, value: int):
        self.rect.left = value

    @property
    def right(self) -> int:
        return self.rect.right

    @right.setter
    def right(self, value: int):
        self.rect.right = value

    @property
    def top(self) -> int:
        return self.rect.top

    @top.setter
    def top(self, value: int):
        self.rect.top = value

    @property
    def bottom(self) -> int:
        return self.rect.bottom

    @bottom.setter
    def bottom(self, value: int):
        self.rect.bottom = value

    def horizontally_center(self, start: int, end: int) -> None:
        """Horizontally center this GenericSprite between two x values"""
        self.left = round(((end + start) - self.size[0]) / 2)

    def vertically_center(self, start: int, end: int) -> None:
        """Vertically center this GenericSprite between two y values"""
        self.top = round(((end + start) - self.size[1]) / 2)


class AnimatedSprite(GenericSprite):

    def __init__(self,
                 anime: animation.Animation,
                 speed=animation.SPEED,
                 animation_loop_state: typing.Optional[animation.LoopState] = None,
                 section_loop_states: typing.Optional[typing.List[animation.LoopState]] = None,
                 starting_frame: typing.Tuple[typing.Optional[int], typing.Optional[int]] = (None, None),
                 kill_when_finished: bool = False,
                 *groups: pygame.sprite.Group,
                 **kwargs):
        super().__init__(image=pygame.Surface((0, 0)), *groups, **kwargs)

        self.animation: animation.Animation = anime
        self.kill_when_finished: bool = kill_when_finished
        self.speed: int = speed

        if section_loop_states is None:
            section_loop_states = [None] * len(self.animation.sections)

        self.section_loop_states = section_loop_states
        self.animation_loop_state = animation_loop_state

        self.__finished: bool = False
        self.__current_frame: int = 0
        self.__animation_iter: typing.Optional[animation.LoopableIter[animation.Section]] = None
        self.__section_iter: typing.Optional[animation.LoopableIter[pygame.Surface]] = None

        self.restart(starting_frame)

    @property
    def finished(self) -> bool:
        return self.__finished

    def restart(self, starting_frame: typing.Tuple[typing.Optional[int], typing.Optional[int]] = (None, None)):
        self.__finished = False

        self.__current_frame = 0
        self.__animation_iter = animation.LoopableIter(self.animation, self.animation_loop_state, starting_frame[0])

        self.next_section(frame=starting_frame[1])

    def next_section(self, loop_state: typing.Optional[animation.LoopState] = None, frame: typing.Optional[int] = None):
        if not self.finished:
            try:
                if loop_state is None:
                    try:
                        loop_state = self.section_loop_states[self.__animation_iter.current_item]
                    except IndexError:
                        pass

                self.__section_iter = animation.LoopableIter(next(self.__animation_iter), loop_state, frame)

            except StopIteration:
                self.__finished = True
                print("END!!!!")

    def update(self, *args):
        super().update(*args)
        if not self.finished:
            if self.__current_frame >= self.speed:
                if not self.__finished:
                    try:
                        self.image = next(self.__section_iter)
                    except StopIteration:
                        self.next_section()
                self.__current_frame = 0
            else:
                self.__current_frame += 1


class MovingSprite(GenericSprite):
    def __init__(self, velocity: typing.Tuple[int, int],
                 *groups: pygame.sprite.Group, **kwargs):
        super().__init__(*groups, **kwargs)

        self.velocity = velocity

    @property
    def dx(self) -> int:
        return self.__dx

    @dx.setter
    def dx(self, value: int):
        self.__dx: int = value

    @property
    def dy(self) -> int:
        return self.__dy

    @dy.setter
    def dy(self, value: int):
        self.__dy: int = value

    @property
    def velocity(self) -> typing.Tuple[int, int]:
        return self.dx, self.dy

    @velocity.setter
    def velocity(self, value: typing.Tuple[int, int]):
        self.dx, self.dy = value

    def update(self, *args):
        super().update(*args)

        self.left += self.dx
        self.top += self.dy


class ScreenSprite(GenericSprite):
    def __init__(self, screen: pygame.Surface, *groups, **kwargs):
        super().__init__(*groups, **kwargs)

        self.screen = screen

        self.__at_bottom: bool = False

    @property
    def screen(self) -> pygame.Surface:
        return self.__screen

    @screen.setter
    def screen(self, value: pygame.Surface):
        self.__screen: pygame.Surface = value
        self.__screen_size: typing.Tuple[int, int] = self.__screen.get_size()

    @property
    def screen_size(self) -> typing.Tuple[int, int]:
        return self.__screen_size

    @property
    def screen_left(self) -> int:
        return 0

    @property
    def screen_right(self) -> int:
        return self.screen_size[0] - 1

    @property
    def screen_top(self) -> int:
        return 0

    @property
    def screen_bottom(self) -> int:
        return self.screen_size[1] - 1

    def on_hit_bottom(self) -> None:
        pass

    def at_top(self) -> bool:
        return self.top <= 0

    def at_bottom(self) -> bool:
        return self.bottom >= self.screen_size[1] - 1

    def at_left(self) -> bool:
        return self.left <= 0

    def at_right(self) -> bool:
        return self.right >= self.screen_size[0] - 1

    def update(self, *args):
        super().update(*args)

        if self.on_hit_bottom is not None:
            bottom = self.at_bottom()
            if not self.__at_bottom and bottom:
                self.on_hit_bottom()

            self.__at_bottom = bottom


class InScreenSprite(ScreenSprite):
    def update(self, *args):
        super().update(*args)

        if self.at_left():
            self.left = self.screen_left
        if self.at_right():
            self.right = self.screen_right
        if self.at_top():
            self.top = self.screen_top
        if self.at_bottom():
            self.bottom = self.screen_bottom


class PlayerAnimationState(enum.IntEnum):
    RUNNING = 0
    TAKING_OFF = 1
    FLYING = 2
    FALLING = 3
    DEAD = 4


class Player(AnimatedSprite, InScreenSprite, MovingSprite):
    ANIMATION = animation.Animation.from_directory(
        os.path.join("assets", "sprites", "player"),
        section_loopstates=[
            animation.LoopState(iterations=-1),
            animation.LoopState(iterations=1),
            animation.LoopState(iterations=-1),
            animation.LoopState(loop_type=animation.LoopType.REPEAT_LAST_FRAME, iterations=-1),
            animation.LoopState(iterations=1)
        ]
    )

    FLY_SPEED = -15
    FALL_SPEED = 15

    def __init__(self, **kwargs):
        super().__init__(anime=self.ANIMATION,
                         velocity=(0, self.FALL_SPEED),
                         kill_when_finished=True,
                         starting_section=PlayerAnimationState.FALLING,
                         **kwargs)

    def on_hit_bottom(self) -> None:
        self.restart((PlayerAnimationState.RUNNING, None))

    @property
    def flying(self) -> bool:
        return self.dy < 0

    @flying.setter
    def flying(self, value: bool):
        if value:
            self.dy = self.FLY_SPEED
            self.restart((PlayerAnimationState.TAKING_OFF, None))
        else:
            self.dy = self.FALL_SPEED
            self.restart((PlayerAnimationState.FALLING, None))

    def update(self, *args):
        super().update(*args)