import sys
import os
import typing

import pygame

import sprites


pygame.init()


def main():
    # D - Display
    screen: pygame.Surface = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Breakout")

    # E - Entities
    dx = 15

    background_images: typing.List[pygame.Surface] = []

    path = os.path.join("assets", "background")

    for files in os.walk(path):
        for file in sorted(files[2]):
            background_images.append(pygame.image.load(os.path.join(path, file)))

    size = 0

    for image in background_images:
        size += image.get_size()[0]

    background = pygame.Surface((size, background_images[0].get_size()[1]))

    position = 0
    for image in background_images:
        background.blit(image, (position, 0))
        position += image.get_size()[0]

    background_position = 0

    del background_images

    player = sprites.Player(screen=screen, position=(round(screen.get_size()[0] * (1 / 8)), 0))
    player.flying = True

    game_sprites = pygame.sprite.Group(player)

    # A - Assign Variables
    clock = pygame.time.Clock()
    keep_going = True

    # Hide the mouse pointer
    pygame.mouse.set_visible(False)

    while keep_going:

        # T - Time
        clock.tick(30)

        # E - Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.flying = True
                if event.key == pygame.K_DOWN:
                    player.flying = False

        # R - Refresh Screen
        game_sprites.clear(screen, background)
        game_sprites.update()

        screen.blit(background, (background_position, 0))
        screen.blit(background, (background_position + background.get_size()[0], 0))

        background_position -= dx

        if background_position + 2 * background.get_size()[0] < screen.get_size()[0]:
            background_position += background.get_size()[0]

        game_sprites.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
