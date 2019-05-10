import pygame
import enum
import typing

import animation


class GenericSprite(pygame.sprite.Sprite):
    """A class to represent generic sprites"""

    # Instance Variables
    image: pygame.Surface
    """Represents the surface that contain the image of this GenericSprite"""

    rect: pygame.Rect
    """Represents the rectangle that is the bounding box of this GenericSprite"""

    # Methods
    def __init__(self, position: typing.Tuple[int, int], image: pygame.Surface, *groups: pygame.sprite.Group):
        """Initializer for the GenericSprite class, sets the image and rect instance variables"""
        super().__init__(*groups)

        self.set_image(image)
        self.set_position(position)

    def get_image(self) -> pygame.Surface:
        """Accessor to return the image of this GenericSprite"""
        return self.image

    def set_image(self, value: pygame.Surface) -> None:
        """Mutator to set the image of this GenericSprite"""
        self.image = value
        self.rect = self.image.get_rect()

    def get_position(self) -> typing.Tuple[int, int]:
        """Accessor to return the position of the top left corner of this GenericSprite"""
        return (self.rect.left, self.rect.top)

    def set_position(self, value: typing.Tuple[int, int]) -> None:
        """Mutator to set position of the top left corner of this GenericSprite"""
        self.rect.left, self.rect.top = value

    def get_top(self) -> int:
        """Accessor to return top position of this GenericSprite"""
        return self.rect.top

    def set_top(self, value: int) -> None:
        """Mutator to set the top position of this GenericSprite"""
        self.rect.top = value

    def get_bottom(self) -> int:
        """Accessor to return bottom position of this GenericSprite"""
        return self.rect.bottom

    def set_bottom(self, value: int) -> None:
        """Mutator to set the bottom position of this GenericSprite"""
        self.rect.bottom = value

    def get_left(self) -> int:
        """Accessor to return left position of this GenericSprite"""
        return self.rect.left

    def set_left(self, value: int) -> None:
        """Mutator to set the left position of this GenericSprite"""
        self.rect.left = value

    def get_right(self) -> int:
        """Accessor to return right position of this GenericSprite"""
        return self.rect.right

    def set_right(self, value: int) -> None:
        """Mutator to set the right position of this GenericSprite"""
        self.rect.right = value

    def get_size(self) -> typing.Tuple[int, int]:
        """Accessor to return the size of this GenericSprite"""
        return self.image.get_size()

    def set_size(self, value: typing.Tuple[int, int]) -> None:
        """Mutator to set the size of this sprite, resizes this GenericSprite using pygame.transform.scale()"""
        self.set_image(pygame.transform.scale(self.image, value))

    def horizontally_center(self, start: int, end: int) -> None:
        """Horizontally center this GenericSprite between two x values"""
        self.set_position((
            round(((end + start) - self.get_size()[0]) / 2),
            self.get_position()[1]
        ))

    def vertically_center(self, start: int, end: int) -> None:
        """Vertically center this GenericSprite between two y values"""
        self.set_position((
            self.get_position()[0],
            round(((end + start) - self.get_size()[1]) / 2)
        ))


class AnimatedSprite(GenericSprite):
    """A class to represent animated sprites. Inherits from GenericSprite"""

    # Instance Variables

    current_section: int
    """Represents the current section the animation is on"""

    current_frame: int
    """Represents the current frame the animation is on"""

    def __init__(self, position: typing.Tuple[int, int], animation: animation.Animation, *groups: pygame.sprite.Group):
        """Initializer for the AnimatedSprite sprite class, sets the sections, directions, and section_loops"""
        super().__init__(position, animation.sections[0].frames[0], *groups)

    def update_state(self):
        pass

    def update(self, *args):
        super().update(*args)


class TextSprite(GenericSprite):
    """A class to represent sprites with text. Used for scorekeeper. Inherits from GenericSprite"""

    # Instance Variables
    font: pygame.font.Font
    # Represents the font for this text sprite

    text: str
    # Represents the text being displayed

    color: pygame.Color
    # Represents the color of the text

    background_color: pygame.Color

    # Represent color behind the text

    # Methods
    def __init__(self, font: pygame.font.Font, text: str, color: pygame.Color, background_color: pygame.Color,
                 position: typing.Tuple[int, int],
                 *groups: pygame.sprite.Group):
        """Initializer for the TextSprite sprite class, sets the font, text, color instance variables"""

    def get_font(self) -> pygame.font.Font:
        """Accessor to return the font of this TextSprite"""

    def set_font(self, value: pygame.font.Font) -> None:
        """Mutator to set the font of this TextSprite"""

    def get_text(self) -> str:
        """Accessor to return the text of this TextSprite"""

    def set_text(self, value: str) -> None:
        """Mutator to set the text of this TextSprite"""

    def get_color(self) -> pygame.Color:
        """Accessor to return the color of this ColoredSprite"""

    def set_color(self, value: pygame.Color) -> None:
        """Mutator to set the color of this ColoredSprite"""

    def get_background_color(self) -> pygame.Color:
        """Accessor to return the background_color of this ColoredSprite"""

    def set_background_color(self, value: pygame.Color) -> None:
        """Mutator to set the background_color of this ColoredSprite"""

    def render(self) -> None:
        """Method to draw the text. Should be called when ever font, text, or color changes"""


class MovingSprite(GenericSprite):
    """A class to represent moving sprites. Inherits from GenericSprite"""

    # Instance Variables
    dx: int
    # The change in the x axis every update

    dy: int

    # The change in the y axis every update

    # Methods
    def __init__(self, dx: int, dy: int, position: typing.Tuple[int, int], image: pygame.Surface,
                 *groups: pygame.sprite.Group):
        """Initializer for the MovingSprite class"""

    def get_dx(self) -> int:
        """Accessor to return the dx of this MovingSprite"""

    def set_dx(self, value: int) -> None:
        """Mutator to set the dx of this MovingSprite"""

    def get_dy(self) -> int:
        """Accessor to return the dy of this MovingSprite"""

    def set_dy(self, value: int) -> None:
        """Mutator to set the dy of this MovingSprite"""

    def update(self, *args) -> None:
        """Update method of this MovingSprite. Changes the sprites position by dx and dy every update"""


class KillIfOutOfScreenSprite(GenericSprite):
    """A class to represent sprites that die after the whole sprite going outside of a surface. Useful for
    ElectricZapper and Missile sprites. Inherits from GenericSprite"""

    # Instance Variables
    screen: pygame.Surface

    # The surface this sprite is rendered on

    # Methods
    def __init__(self, screen: pygame.Surface, position: typing.Tuple[int, int], image: pygame.Surface,
                 *groups: pygame.sprite.Group):
        """Initializer for the KillIfOutOfScreenSprite class"""

    def update(self, *args) -> None:
        """Check if itself is outside of its surface. If it is, kills itself."""


class InScreenSprite(GenericSprite):
    """A class to represent sprites that can't go outside of a surface. Inherits from GenericSprite"""
    # Instance Variables
    screen: pygame.Surface

    # The surface this sprite is rendered on

    # Methods
    def __init__(self, screen: pygame.Surface, position: typing.Tuple[int, int], image: pygame.Surface,
                 *groups: pygame.sprite.Group):
        """Initializer for the InScreenSprite class"""

    def update(self, *args) -> None:
        """Update method of this InScreenSprite. Calls parent's update and sets the position to the
        edge if it goes out of an edge"""


class Player(MovingSprite, InScreenSprite):
    """A class to represent players sprites. Inherits from GenericSprite, InScreenSprite."""

    # Instance Variables
    JETPACK_ON_IMAGE: pygame.Surface
    # The image when the jetpack is on

    JETPACK_OFF_IMAGE: pygame.Surface
    # The image when the jetpack is off

    powerup: bool
    # The player is power up state

    powerup_duration: int

    # The remaining duration of the player's power up in sections

    # Methods
    def __init__(self, position: typing.Tuple[int, int], *groups: pygame.sprite.Group):
        """Initializer for the Player sprite class. Call the superclass's constructor with JETPACK_OFF_IMAGE to set the
        image"""

    def get_powerup(self) -> bool:
        """Accessor to return the powerup of this Player"""

    def set_powerup(self, value: bool) -> None:
        """Mutator to set the powerup of this Player. If the value is False set the powerup_duration to 0"""

    def get_powerup_duration(self) -> int:
        """Accessor to return the powerup_duration of this Player"""

    def set_powerup_duration(self, value: bool) -> None:
        """Mutator to set the powerup_duration of this Player. If the value more than 0 set powerup to True, otherwise
        set it to False"""

    def update(self, *args) -> None:
        """Set image to JETPACK_ON_IMAGE if dy < 0, else sets image to JETPACK_OFF_IMAGE.
        Subtracts 1 from powerup_duration every update until it reaches 0, then set powerup to False"""


class ElectricZapper(MovingSprite, KillIfOutOfScreenSprite):
    """A class to represent an electric zapper. Inherits from MovingSprite, KillIfOutOfScreenSprite. It's moving
    because it moves instead of the player giving the player the illusion of moving. """

    # Instance Variables
    IMAGE: pygame.Surface

    # The default image for this sprite

    # Methods
    def __init__(self, screen: pygame.Surface, dx: int, dy: int, position: tuple, *groups: pygame.sprite.Group):
        """Initializer for the ElectricZapper class. Call the superclasses' constructors with IMAGE to set the image"""


class Missile(MovingSprite, KillIfOutOfScreenSprite):
    """A class to represent an missile. Inherits from MovingSprite, KillIfOutOfScreenSprite. """

    # Instance Variables
    WARNING_IMAGE: pygame.Surface
    # The image displayed as a warning to the player

    IMAGE: pygame.Surface
    # The default image for this sprite

    warning_duration: int
    # The duration of the warning is displayed for in sections

    firing_velocity: typing.Tuple[int, int]

    # Velocity the missile is being fired at

    # Methods
    def __init__(self, screen: pygame.Surface, dx: int, dy: int, warning_duration: int,
                 position: typing.Tuple[int, int],
                 *groups: pygame.sprite.Group):
        """Initializer for the Missile class. Sets the warning duration, sets the firing_velocity to (dx, dy), and calls
        the superclasses' constructors with WARNING_IMAGE to set the image"""

    def update(self, *args) -> None:
        """Subtracts 1 from warning_duration every update until it reaches 0, then set the image to IMAGE and sets the
        velocity to firing_velocity"""


class PowerUp(MovingSprite, KillIfOutOfScreenSprite):
    """A class to represent an electric zapper. Inherits from MovingSprite, KillIfOutOfScreenSprite. It's moving
    because it moves instead of the player giving the player the illusion of moving. """

    # Instance Variables
    IMAGE: pygame.Surface

    # The default image for this sprite

    # Methods
    def __init__(self, screen: pygame.Surface, dx: int, dy: int, position: typing.Tuple[int, int],
                 *groups: pygame.sprite.Group):
        """Initializer for the PowerUp class. Call the superclasses' constructors with IMAGE to set the image"""


class ScoreKeeper(TextSprite):
    """A class to represent the scorekeeper"""
    # Instance Variables
    TEXT: str
    # Format string of the scoreboard

    score: int

    # The score being displayed which is the distance traveled

    # Methods
    def __init__(self, font: pygame.font.Font, color: pygame.Color, background_color: pygame.Color,
                 position: typing.Tuple[int, int],
                 *groups: pygame.sprite.Group):
        """Initializer for the ScoreKeeper class. Calls
        the superclasses' constructors with TEXT % (score, ) to set the text"""

    def get_score(self) -> int:
        """Accessor to return the score of this ScoreKeeper"""

    def set_score(self, value) -> None:
        """Mutator to set the score of this ScoreKeeper. Calls render()"""
