""" Author: Jun Bo Bi
    Date: May 29, 2019
    Desc: Game Sprites
"""
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
    """A class representing generic sprites, inherits from pygame.sprite.Sprite"""

    def __init__(self, image: pygame.Surface, position: typing.Tuple[int, int], layer: int = 0,
                 *groups: pygame.sprite.Group, **kwargs):
        """Initializer for the GenericSprite class"""
        super().__init__(*groups)

        self.image = image
        self.position = position
        self.layer = layer

    @property
    def image(self) -> pygame.Surface:
        """Getter for the image attribute for this GenericSprite"""
        return self.__image

    @image.setter
    def image(self, value: pygame.Surface):
        """Setter for the image attribute for this GenericSprite"""
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
        """Getter for the rect attribute for this GenericSprite"""
        return self.__rect

    @property
    def mask(self) -> pygame.mask.Mask:
        """Getter for the mask attribute for this GenericSprite"""
        return self.__mask

    @property
    def size(self) -> typing.Tuple[int, int]:
        """Getter for the size attribute for this GenericSprite"""
        return self.image.get_size()

    @size.setter
    def size(self, value: typing.Tuple[int, int]):
        """Setter for the size attribute for this GenericSprite"""
        self.image = pygame.transform.scale(self.image, value)

    @property
    def position(self) -> typing.Tuple[int, int]:
        """Getter for the position attribute for this GenericSprite"""
        return self.rect.left, self.rect.top

    @position.setter
    def position(self, value: typing.Tuple[int, int]):
        """Setter for the position attribute for this GenericSprite"""
        self.rect.left, self.rect.top = value

    @property
    def left(self) -> int:
        """Getter for the left position of this GenericSprite"""
        return self.rect.left

    @left.setter
    def left(self, value: int):
        """Setter for the left position of this GenericSprite"""
        self.rect.left = value

    @property
    def right(self) -> int:
        """Getter for the right position of this GenericSprite"""
        return self.rect.right

    @right.setter
    def right(self, value: int):
        """Setter for the left position of this GenericSprite"""
        self.rect.right = value

    @property
    def top(self) -> int:
        """Getter for the top position of this GenericSprite"""
        return self.rect.top

    @top.setter
    def top(self, value: int):
        """Setter for the top position of this GenericSprite"""
        self.rect.top = value

    @property
    def bottom(self) -> int:
        """Getter for the bottom position of this GenericSprite"""
        return self.rect.bottom

    @bottom.setter
    def bottom(self, value: int):
        """Setter for the bottom position of this GenericSprite"""
        self.rect.bottom = value

    @property
    def layer(self) -> int:
        """Getter for the layer number of this GenericSprite"""
        return self._layer

    @layer.setter
    def layer(self, value: int):
        """Setter for the layer number of this GenericSprite"""
        self._layer = value

    def horizontally_center(self, start: int, end: int) -> None:
        """Horizontally center this GenericSprite between two x values"""
        self.left = round(((end + start) - self.size[0]) / 2)

    def vertically_center(self, start: int, end: int) -> None:
        """Vertically center this GenericSprite between two y values"""
        self.top = round(((end + start) - self.size[1]) / 2)


class AnimatedSprite(GenericSprite):
    """A class representing animated sprites, inherits from GenericSprite"""
    def __init__(self,
                 anime: animation.Animation,
                 speed=animation.SPEED,
                 animation_loop_state: typing.Optional[animation.LoopState] = None,
                 section_loop_states: typing.Optional[typing.List[animation.LoopState]] = None,
                 starting_frame: typing.Tuple[typing.Optional[int], typing.Optional[int]] = (None, None),
                 kill_when_finished: bool = False,
                 *groups: pygame.sprite.Group,
                 **kwargs):
        """Initializer for AnimatedSprite class"""

        super().__init__(image=pygame.Surface((0, 0)), *groups, **kwargs)

        self.animation: animation.Animation = anime
        self.kill_when_finished: bool = kill_when_finished
        self.speed: int = speed

        if section_loop_states is None:
            section_loop_states = [None] * len(self.animation.sections)

        self.section_loop_states: typing.List[typing.Optional[animation.LoopState]] = section_loop_states
        self.animation_loop_state: typing.Optional[animation.LoopState] = animation_loop_state

        self.__finished: bool = False
        self.__frames_passed: int = 0
        self.__animation_iter: typing.Optional[animation.LoopableIter[animation.Section]] = None
        self.__section_iter: typing.Optional[animation.LoopableIter[pygame.Surface]] = None

        self.restart(starting_frame)

    @property
    def finished(self) -> bool:
        """Getter for weather the animation is finished"""
        return self.__finished

    def restart(self, starting_frame: typing.Tuple[typing.Optional[int], typing.Optional[int]] = (None, None)):
        """Restart the animation, the starting section and frame could optionally be specified is a tuple of two ints"""
        self.__finished = False

        self.__frames_passed = 0
        self.__animation_iter = animation.LoopableIter(self.animation, self.animation_loop_state, starting_frame[0])

        self.next_section(frame=starting_frame[1])

    def next_section(self, loop_state: typing.Optional[animation.LoopState] = None, frame: typing.Optional[int] = None):
        """Go to the next section"""
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
        """Update method for AnimatedSprite"""
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
    def __init__(self, velocity: typing.Tuple[int, int], *groups: pygame.sprite.Group, **kwargs):
        """A class representing moving sprites, inherits from GenericSprite"""
        super().__init__(*groups, **kwargs)

        self.velocity = velocity

    @property
    def dx(self) -> int:
        """Getter for the delta x per frame attribute of this MovingSprite"""
        return self.__dx

    @dx.setter
    def dx(self, value: int):
        """Setter for the delta x per frame attribute of this MovingSprite"""
        self.__dx: int = value

    @property
    def dy(self) -> int:
        """Getter for the delta y per frame attribute of this MovingSprite"""
        return self.__dy

    @dy.setter
    def dy(self, value: int):
        """Setter for the delta y per frame attribute of this MovingSprite"""
        self.__dy: int = value

    @property
    def velocity(self) -> typing.Tuple[int, int]:
        """Getter for the velocity attribute of this MovingSprite"""
        return self.dx, self.dy

    @velocity.setter
    def velocity(self, value: typing.Tuple[int, int]):
        """Getter for the velocity attribute of this MovingSprite"""
        self.dx, self.dy = value

    def update(self, *args):
        """Update method for this MovingSprite"""
        super().update(*args)

        self.left += self.dx
        self.top += self.dy


class AcceleratingSprite(MovingSprite):
    """A class representing accelerating sprites, inherits from MovingSprite"""
    def __init__(self, acceleration: typing.Tuple[int, int], *groups, **kwargs):
        """Initializer for the AcceleratingSprite class"""
        super().__init__(velocity=(0, 0), *groups, **kwargs)

        self.acceleration = acceleration

    @property
    def ddx(self) -> int:
        """Getter for the delta dx per frame attribute of this AcceleratingSprite"""
        return self.__ddx

    @ddx.setter
    def ddx(self, value: int):
        """Setter for the delta dx per frame attribute of this AcceleratingSprite"""
        self.__ddx: int = value

    @property
    def ddy(self) -> int:
        """Getter for the delta dy per frame attribute of this AcceleratingSprite"""
        return self.__ddy

    @ddy.setter
    def ddy(self, value: int):
        """Setter for the delta dy per frame attribute of this AcceleratingSprite"""
        self.__ddy: int = value

    @property
    def acceleration(self) -> typing.Tuple[int, int]:
        """Getter for the acceleration attribute of this AcceleratingSprite"""
        return self.ddx, self.ddy

    @acceleration.setter
    def acceleration(self, value: typing.Tuple[int, int]):
        """Setter for the acceleration attribute of this AcceleratingSprite"""
        self.ddx, self.ddy = value

    def update(self, *args):
        """Update method for this AcceleratingSprite"""
        super().update(*args)

        self.dx += self.ddx
        self.dy += self.ddy


class ScreenSprite(GenericSprite):
    """A class representing screen sprites, inherits from GenericSprite"""
    def __init__(self, screen: pygame.Surface, *groups, **kwargs):
        """Initializer for the ScreenSprite class"""
        super().__init__(*groups, **kwargs)

        self.screen = screen

        self.__at_bottom: bool = False
        self.__at_top: bool = False

    @property
    def screen(self) -> pygame.Surface:
        """Getter for the screen attribute of this ScreenSprite"""
        return self.__screen

    @screen.setter
    def screen(self, value: pygame.Surface):
        """Setter for the screen attribute of this ScreenSprite"""
        self.__screen: pygame.Surface = value
        self.__screen_size: typing.Tuple[int, int] = self.__screen.get_size()

    @property
    def screen_size(self) -> typing.Tuple[int, int]:
        """Getter for the screen_size attribute of this ScreenSprite"""
        return self.__screen_size

    @property
    def screen_left(self) -> int:
        """Getter for the screen_left attribute of this ScreenSprite"""
        return 0

    @property
    def screen_right(self) -> int:
        """Getter for the screen_right attribute of this ScreenSprite"""
        return self.screen_size[0] - 1

    @property
    def screen_top(self) -> int:
        """Getter for the screen_top attribute of this ScreenSprite"""
        return 0

    @property
    def screen_bottom(self) -> int:
        """Getter for the screen_bottom attribute of this ScreenSprite"""
        return self.screen_size[1] - 1

    def on_hit_bottom(self) -> None:
        """Called when this ScreenSprite hits the bottom of the screen"""
        pass

    def on_hit_top(self) -> None:
        """Called when this ScreenSprite hits the top if the screen"""
        pass

    def at_top(self) -> bool:
        """Returns if this ScreenSprite is at the top of the screen"""
        return self.top <= self.screen_top

    def at_bottom(self) -> bool:
        """Returns if this ScreenSprite is at the bottom of the screen"""
        return self.bottom >= self.screen_bottom

    def at_left(self) -> bool:
        """Returns if this ScreenSprite is at the left of the screen"""
        return self.left <= self.screen_left

    def at_right(self) -> bool:
        """Returns if this ScreenSprite is at the right of the screen"""
        return self.right >= self.screen_right

    def outside_top(self):
        """Returns if this ScreenSprite is outside the top of the screen"""
        return self.bottom < self.screen_top

    def outside_bottom(self):
        """Returns if this ScreenSprite is outside the bottom of the screen"""
        return self.top > self.screen_bottom

    def outside_left(self):
        """Returns if this ScreenSprite is outside the left of the screen"""
        return self.right < self.screen_left

    def outside_right(self):
        """Returns if this ScreenSprite is outside the right of the screen"""
        return self.left > self.screen_right

    def outside(self):
        """Returns if this ScreenSprite is outside the screen"""
        return self.outside_top() or self.outside_bottom() or self.outside_left() or self.outside_right()

    def update(self, *args):
        """update method for this ScreenSprite"""
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
    """A class representing in screen sprites"""

    def update(self, *args):
        """update method for this InScreenSprite"""
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
    """A class representing sprites that die if it goes out of screen, inherits from ScreenSprite"""

    def update(self, *args):
        """update method for this KillIfOutOfScreenSprite"""
        super().update(*args)

        if self.outside():
            self.kill()


class TextSprite(GenericSprite):
    """A class representing text sprites, inherits from GenericSprite"""

    def __init__(self, font: pygame.font.Font, text: str,
                 color: pygame.Color = pygame.Color(0, 0, 0, 0),
                 background_color: typing.Optional[pygame.Color] = None,
                 antialias: bool = False,
                 *groups,
                 **kwargs):
        """Initializer for the TextSprite class"""
        super().__init__(image=pygame.Surface((0, 0)), *groups, **kwargs)

        self.font = font
        self.text = text
        self.color = color
        self.background_color = background_color
        self.antialias = antialias

    @property
    def font(self) -> pygame.font.Font:
        """Getter for the font attribute of this TextSprite"""
        return self.__font

    @font.setter
    def font(self, value: pygame.font.Font):
        """Setter for the font attribute of this TextSprite"""
        self.__font: pygame.font.Font = value
        self.render()

    @property
    def text(self) -> str:
        """Getter for the text attribute of this TextSprite"""
        return self.__text

    @text.setter
    def text(self, value: str):
        """Setter for the text attribute of this TextSprite"""
        self.__text: str = value
        self.render()

    @property
    def color(self) -> pygame.Color:
        """Getter for the color attribute of this TextSprite"""
        return self.__color

    @color.setter
    def color(self, value: pygame.Color):
        """Setter for the color attribute of this TextSprite"""
        self.__color: pygame.Color = value
        self.render()

    @property
    def background_color(self) -> pygame.Color:
        """Getter for the background_color attribute of this TextSprite"""
        return self.__background_color

    @background_color.setter
    def background_color(self, value: pygame.Color):
        """Setter for the font attribute of this TextSprite"""
        self.__background_color: pygame.Color = value
        self.render()

    @property
    def antialias(self) -> bool:
        """Getter for the antialias attribute of this TextSprite"""
        return self.__antialias

    @antialias.setter
    def antialias(self, value: bool):
        """Setter for the antialias attribute of this TextSprite"""
        self.__antialias = value
        self.render()

    def render(self):
        """render method for this TextSprite"""
        try:
            self.image = self.font.render(self.text, self.antialias, self.color, self.background_color)
        except AttributeError:
            pass


class BackgroundSprite(ScreenSprite, MovingSprite):
    """A class representing background sprites, inherits from ScreenSprite, MovingSprite"""

    def __init__(self, images: typing.Iterable[pygame.Surface], direction: bool = True, *groups, **kwargs):
        """
        Initializer for the GenericSprite class
        images: images that combine to form the background
        direction: True if horizontal, False if vertical
        """
        super().__init__(image=pygame.Surface((0, 0)), position=(0, 0), layer=-1, *groups, **kwargs)

        self.direction: bool = direction

        sizes: typing.List[typing.Tuple[int, int]] = list(map(lambda img: img.get_size(), images))
        widths, heights = zip(*sizes)

        # Primary is the length of direction of the background's movement
        if self.direction:
            primaries, secondaries = widths, heights
        else:
            primaries, secondaries = heights, widths

        # Calculate the width and height of the sprite
        primary, secondary = sum(primaries), max(secondaries)

        repeat = math.ceil(self.screen_size[0] / primary) * 2
        primary *= repeat

        size = (primary, secondary) if self.direction else (secondary, primary)

        self.image = pygame.Surface(
            size,
            pygame.SRCALPHA
        )

        x, y = 0, 0

        # Blit the images in order
        for _ in range(repeat):
            for image, size in zip(images, sizes):
                self.image.blit(image, (x, y))
                if self.direction:
                    x += size[0]
                else:
                    y += size[1]

    def update(self, *args):
        """update method for this BackgroundSprite"""
        super().update()

        if not self.at_left():
            self.left -= self.size[0] // 2

        if not self.at_right():
            self.right += self.size[0] // 2

        if not self.at_top():
            self.left -= self.size[0] // 2

        if not self.at_bottom():
            self.right += self.size[0] // 2


class Scoreboard(TextSprite):
    """A class representing scoreboard sprites, inherits from TextSprite"""

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
        """
        Initializer for the Scoreboard class
        unit: the unit per distance
        """

        super().__init__(
            font=font, text=text, color=color, antialias=antialias, position=position, layer=100, *groups, **kwargs
        )

        self.unit: int = unit
        self.score_text: str = score_text
        self.pixels = pixels

    @property
    def pixels(self) -> int:
        """Getter for the length in pixels of the player's distance of this Scoreboard"""
        return self.__pixels

    @pixels.setter
    def pixels(self, value: int):
        """Setter for the length in pixels of the player's distance of this Scoreboard"""
        self.__pixels: int = value

        self.text = self.score_text % round(self.distance)

    @property
    def distance(self) -> float:
        """Getter for the length in distance of the player's distance of this Scoreboard"""
        return self.pixels / self.unit

    @distance.setter
    def distance(self, value: float):
        """Setter for the length in distance of the player's distance of this Scoreboard"""
        self.pixels = round(value * self.unit)


class PlayerAnimationState(enum.IntEnum):
    """A class representing player animation states"""

    RUNNING = 0
    TAKING_OFF = 1
    FLYING = 2
    FALLING = 3
    DEAD = 4


class Player(AnimatedSprite, InScreenSprite, AcceleratingSprite):
    """A class representing player sprites, inherits from AnimatedSprite, InScreenSprite, AcceleratingSprite"""

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
        """Initializer for the Player class"""
        super().__init__(anime=self.ANIMATION,
                         acceleration=(0, self.FALL_ACCELERATION),
                         kill_when_finished=True,
                         starting_section=PlayerAnimationState.FALLING,
                         **kwargs)

        self.jetpack_on_sound = pygame.mixer.Sound(os.path.join("assets", "audio", "jetpack_on.wav"))
        self.death_sound = pygame.mixer.Sound(os.path.join("assets", "audio", "death.wav"))

        self.dead = False

    def on_hit_bottom(self) -> None:
        """on_hit_bottom method for this Player"""
        if not self.dead and not self.flying:
            self.restart((PlayerAnimationState.RUNNING, None))

        self.dy = 0

    def on_hit_top(self) -> None:
        """on_hit_top method for this Player"""
        self.dy = 0

    @property
    def flying(self) -> bool:
        """Getter for the flying attribute of this Player"""
        return self.ddy < 0

    @flying.setter
    def flying(self, value: bool):
        """Setter for the flying attribute of this Player"""
        if not self.dead:
            if value:
                self.ddy = self.FLY_ACCELERATION
                self.restart((PlayerAnimationState.TAKING_OFF, None))
                self.jetpack_on_sound.play(-1)
            else:
                self.ddy = self.FALL_ACCELERATION
                self.restart((PlayerAnimationState.FALLING, None))
                self.jetpack_on_sound.stop()

    @property
    def dead(self) -> bool:
        """Getter for the dead attribute of this Player"""
        return self.__dead

    @dead.setter
    def dead(self, value: bool):
        """Setter for the dead attribute of this Player"""
        self.__dead: bool = value
        if value:
            self.restart((PlayerAnimationState.DEAD, None))
            self.ddy = self.FALL_ACCELERATION

            self.death_sound.play()
            self.jetpack_on_sound.stop()

    def update(self, *args):
        """update method for this Player"""
        super().update(*args)
        if not self.dead:
            if self.at_top() and self.ddy < 0:
                self.dy = 0
                self.ddy = 0
            elif self.at_bottom() and self.ddy > 0:
                self.dy = 0
                self.ddy = 0


class Zapper(MovingSprite, KillIfOutOfScreenSprite):
    """A class representing zapper sprites, inherits from MovingSprite, KillIfOutOfScreenSprite"""

    IMAGES: typing.Tuple[pygame.Surface, ...] = tuple(
        next(helper.load_images(os.path.join("assets", "sprites", "zapper")))
    )

    def __init__(self, orientation: bool = True, direction: bool = True, *groups, **kwargs):

        """
        Initializer for the Zapper class
        orientation: on if True, else False
        direction: horizontal if True, else vertical
        """
        super().__init__(image=self.IMAGES[0], *groups, **kwargs)

        self.orientation = orientation
        self.direction = direction

    @classmethod
    def random_spawn(cls, screen: pygame.Surface, *groups, **kwargs):
        """Randomly spawns a zapper in a random location and orientation"""
        instance = cls(screen=screen, position=(0, 0), direction=helper.chance(0.5), *groups, **kwargs)
        instance.position = (screen.get_size()[0] - 1, random.randrange(0, screen.get_size()[1] - instance.size[1]))

        return instance

    @property
    def orientation(self) -> bool:
        """Getter for the orientation attribute of this Zapper"""
        return self.__orientation

    @orientation.setter
    def orientation(self, value: bool):
        """Setter for the orientation attribute of this Zapper"""
        self.__orientation: bool = value
        self.__update_image()

    @property
    def direction(self) -> bool:
        """Getter for the direction attribute of this Zapper"""
        return self.__direction

    @direction.setter
    def direction(self, value: bool):
        """Setter for the direction attribute of this Zapper"""
        self.__direction: bool = value
        self.__update_image()

    def __update_image(self):
        """update_image method for this Zapper"""
        try:
            if self.orientation:
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
