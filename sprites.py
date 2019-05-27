import os
import math
import random
import enum
import typing

import pygame

import helper
import animation

pygame.font.init()


class GenericSprite(pygame.sprite.Sprite):
    """A class to represent generic sprites"""

    def __init__(self, image: pygame.Surface, position: typing.Tuple[int, int], layer: int = 0,
                 *groups: pygame.sprite.Group, **kwargs):
        """Initializer for the GenericSprite class, sets the image and rect instance variables"""
        super().__init__(*groups)

        self.image = image
        self.position = position
        self.layer = layer

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
        self.__mask: pygame.mask.Mask = pygame.mask.from_surface(self.image)

        self.position = position

    @property
    def rect(self) -> pygame.Rect:
        return self.__rect

    @property
    def mask(self) -> pygame.mask.Mask:
        return self.__mask

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

    @property
    def layer(self) -> int:
        return self._layer

    @layer.setter
    def layer(self, value: int):
        self._layer = value

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
        self.__frames_passed: int = 0
        self.__animation_iter: typing.Optional[animation.LoopableIter[animation.Section]] = None
        self.__section_iter: typing.Optional[animation.LoopableIter[pygame.Surface]] = None

        self.restart(starting_frame)

    @property
    def finished(self) -> bool:
        return self.__finished

    def restart(self, starting_frame: typing.Tuple[typing.Optional[int], typing.Optional[int]] = (None, None)):
        self.__finished = False

        self.__frames_passed = 0
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

    def update(self, *args):
        super().update(*args)
        if not self.finished:
            if self.__frames_passed >= self.speed:
                if not self.__finished:
                    try:
                        self.image = next(self.__section_iter)
                    except StopIteration:
                        self.next_section()
                self.__frames_passed = 0
            else:
                self.__frames_passed += 1


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


class AcceleratingSprite(MovingSprite):
    def __init__(self, acceleration: typing.Tuple[int, int], *groups, **kwargs):
        super().__init__(velocity=(0, 0), *groups, **kwargs)

        self.acceleration = acceleration

    @property
    def ddx(self) -> int:
        return self.__ddx

    @ddx.setter
    def ddx(self, value: int):
        self.__ddx: int = value

    @property
    def ddy(self) -> int:
        return self.__ddy

    @ddy.setter
    def ddy(self, value: int):
        self.__ddy: int = value

    @property
    def acceleration(self) -> typing.Tuple[int, int]:
        return self.ddx, self.ddy

    @acceleration.setter
    def acceleration(self, value: typing.Tuple[int, int]):
        self.ddx, self.ddy = value

    def update(self, *args):
        super().update(*args)

        self.dx += self.ddx
        self.dy += self.ddy


class ScreenSprite(GenericSprite):
    def __init__(self, screen: pygame.Surface, *groups, **kwargs):
        super().__init__(*groups, **kwargs)

        self.screen = screen

        self.__at_bottom: bool = False
        self.__at_top: bool = False

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

    def on_hit_top(self) -> None:
        pass

    def at_top(self) -> bool:
        return self.top <= 0

    def at_bottom(self) -> bool:
        return self.bottom >= self.screen_size[1] - 1

    def at_left(self) -> bool:
        return self.left <= 0

    def at_right(self) -> bool:
        return self.right >= self.screen_size[0] - 1

    def outside_top(self):
        return self.bottom < self.screen_top

    def outside_bottom(self):
        return self.top > self.screen_bottom

    def outside_left(self):
        return self.right < self.screen_left

    def outside_right(self):
        return self.left > self.screen_right

    def outside(self):
        return self.outside_top() or self.outside_bottom() or self.outside_left() or self.outside_right()

    def update(self, *args):
        super().update(*args)

        bottom = self.at_bottom()
        top = self.at_top()

        if not self.__at_bottom and bottom:
            self.on_hit_bottom()

        if not self.__at_top and top:
            self.on_hit_top()

        self.__at_bottom = bottom
        self.__at_top = top


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


class KillIfOutOfScreenSprite(ScreenSprite):
    def update(self, *args):
        super().update(*args)

        if self.outside():
            self.kill()


class TextSprite(GenericSprite):
    def __init__(self,
                 font: pygame.font.Font,
                 text: str,
                 color: pygame.Color = pygame.Color(0, 0, 0, 0),
                 background_color: typing.Optional[pygame.Color] = None,
                 antialias: bool = False,
                 *groups,
                 **kwargs):
        super().__init__(image=pygame.Surface((0, 0)), *groups, **kwargs)

        self.font = font
        self.text = text
        self.color = color
        self.background_color = background_color
        self.antialias = antialias

    @property
    def font(self) -> pygame.font.Font:
        return self.__font

    @font.setter
    def font(self, value: pygame.font.Font):
        self.__font: pygame.font.Font = value
        self.render()

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value: str):
        self.__text: str = value
        self.render()

    @property
    def color(self) -> pygame.Color:
        return self.__color

    @color.setter
    def color(self, value: pygame.Color):
        self.__color: pygame.Color = value
        self.render()

    @property
    def background_color(self) -> pygame.Color:
        return self.__background_color

    @background_color.setter
    def background_color(self, value: pygame.Color):
        self.__background_color: pygame.Color = value
        self.render()

    @property
    def antialias(self) -> bool:
        return self.__antialias

    @antialias.setter
    def antialias(self, value: bool):
        self.__antialias = value
        self.render()

    def render(self):
        try:
            self.image = self.font.render(self.text, self.antialias, self.color, self.background_color)
        except AttributeError:
            pass


class Scoreboard(TextSprite):
    def __init__(self,
                 font: pygame.font.Font = helper.default_font(32),
                 text: str = "",
                 color: pygame.Color = pygame.Color(255, 255, 255),
                 antialias: bool = True,
                 position: typing.Tuple[int, int] = (0, 0),
                 pixels: int = 0,
                 unit: int = 50,
                 score_text: str = "Distance: %d",
                 *groups, **kwargs):
        super().__init__(
            font=font,
            text=text,
            color=color,
            antialias=antialias,
            position=position,
            layer=100,
            *groups,
            **kwargs
        )

        self.unit: int = unit
        self.score_text: str = score_text
        self.pixels = pixels

    @property
    def pixels(self) -> int:
        return self.__pixels

    @pixels.setter
    def pixels(self, value: int):
        self.__pixels: int = value

        self.text = self.score_text % round(self.distance)

    @property
    def distance(self) -> float:
        return self.pixels / self.unit

    @distance.setter
    def distance(self, value: float):
        self.pixels = round(value * self.unit)


class BackgroundSprite(ScreenSprite):

    def __init__(self, screen: pygame.Surface, images: typing.Iterable[pygame.Surface], speed: int,
                 direction: bool = True, *groups, **kwargs):
        """direction: True if horizontal, False if vertical"""
        super().__init__(image=pygame.Surface(screen.get_size(), pygame.SRCALPHA), position=(0, 0), screen=screen,
                         layer=-1, *groups,
                         **kwargs)

        self.speed: int = speed
        self.background_position: int = 0
        self.direction: bool = direction

        sizes: typing.List[typing.Tuple[int, int]] = list(map(lambda img: img.get_size(), images))
        widths, heights = (size[0] for size in sizes), (size[1] for size in sizes)

        if self.direction:
            width, height = sum(widths), max(heights)

            repeat = math.ceil(self.screen_size[0] / width)
            width *= repeat
        else:
            width, height = max(widths), sum(heights)

            repeat = math.ceil(self.screen_size[1] / height)
            height *= repeat

        self.__background: pygame.Surface = pygame.Surface((width, height), pygame.SRCALPHA)

        x, y = 0, 0

        for _ in range(repeat):
            for image, size in zip(images, sizes):
                self.__background.blit(image, (x, y))
                if self.direction:
                    x += size[0]
                else:
                    y += size[1]

    def update(self, *args):
        if self.direction:
            length = self.__background.get_size()[0]
            minimum = self.screen_left
            maximum = self.screen_right
        else:
            length = self.__background.get_size()[1]
            minimum = self.screen_top
            maximum = self.screen_bottom

        if self.background_position > minimum:
            self.background_position -= length

        if self.background_position + 2 * length < maximum:
            self.background_position += length

        if self.direction:
            position = (self.background_position, 0)
            position2 = (self.background_position + length, 0)
        else:
            position = (0, self.background_position)
            position2 = (self.background_position + length, 0)

        self.image.fill(pygame.SRCALPHA)
        self.image.blit(self.__background, position)
        self.image.blit(self.__background, position2)

        self.background_position += self.speed


class PlayerAnimationState(enum.IntEnum):
    RUNNING = 0
    TAKING_OFF = 1
    FLYING = 2
    FALLING = 3
    DEAD = 4


class Player(AnimatedSprite, InScreenSprite, AcceleratingSprite):
    ANIMATION = animation.Animation.from_directory(
        os.path.join("assets", "sprites", "player"),
        section_loopstates=[
            animation.LoopState(iterations=-1),
            animation.LoopState(iterations=1),
            animation.LoopState(iterations=-1),
            animation.LoopState(loop_type=animation.LoopType.REPEAT_LAST_FRAME, iterations=-1),
            animation.LoopState(loop_type=animation.LoopType.REPEAT_LAST_FRAME, iterations=-1)
        ]
    )

    FLY_ACCELERATION = -0.5
    FALL_ACCELERATION = 0.5

    def __init__(self, **kwargs):
        super().__init__(anime=self.ANIMATION,
                         acceleration=(0, self.FALL_ACCELERATION),
                         kill_when_finished=True,
                         starting_section=PlayerAnimationState.FALLING,
                         **kwargs)

        self.dead = False

    def on_hit_bottom(self) -> None:
        if not self.dead and not self.flying:
            self.restart((PlayerAnimationState.RUNNING, None))

        self.dy = 0

    def on_hit_top(self) -> None:
        self.dy = 0

    @property
    def flying(self) -> bool:
        return self.ddy < 0

    @flying.setter
    def flying(self, value: bool):
        if not self.dead:
            if value:
                self.ddy = self.FLY_ACCELERATION
                self.restart((PlayerAnimationState.TAKING_OFF, None))
            else:
                self.ddy = self.FALL_ACCELERATION
                self.restart((PlayerAnimationState.FALLING, None))

    @property
    def dead(self) -> bool:
        return self.__dead

    @dead.setter
    def dead(self, value: bool):
        self.__dead: bool = value
        if value:
            self.restart((PlayerAnimationState.DEAD, None))
            self.ddy = self.FALL_ACCELERATION

    def update(self, *args):
        super().update(*args)
        if not self.dead:
            if self.at_top() and self.ddy < 0:
                self.dy = 0
                self.ddy = 0
            elif self.at_bottom() and self.ddy > 0:
                self.dy = 0
                self.ddy = 0


class Zapper(MovingSprite, KillIfOutOfScreenSprite):
    IMAGES: typing.Tuple[pygame.Surface, ...] = tuple(
        next(helper.load_images(os.path.join("assets", "sprites", "zapper")))
    )

    def __init__(self, state: bool = True, direction: bool = True, *groups, **kwargs):
        """direction: horizontal if True, else vertical"""
        super().__init__(image=self.IMAGES[0], *groups, **kwargs)

        self.state = state
        self.direction = direction

    @classmethod
    def random_spawn(cls, screen: pygame.Surface, *groups, **kwargs):
        instance = cls(screen=screen, position=(0, 0), direction=helper.chance(0.5), *groups, **kwargs)
        instance.position = (screen.get_size()[0] - 1, random.randrange(0, screen.get_size()[1] - instance.size[1]))

        return instance

    @property
    def state(self) -> bool:
        return self.__state

    @state.setter
    def state(self, value: bool):
        self.__state: bool = value
        self.__update_image()

    @property
    def direction(self) -> bool:
        return self.__direction

    @direction.setter
    def direction(self, value: bool):
        self.__direction: bool = value
        self.__update_image()

    def __update_image(self):
        try:
            if self.state:
                if self.direction:
                    self.image = self.IMAGES[1]
                else:
                    self.image = self.IMAGES[3]
            else:
                if self.direction:
                    self.image = self.IMAGES[0]
                else:
                    self.image = self.IMAGES[2]

        except AttributeError:
            pass
