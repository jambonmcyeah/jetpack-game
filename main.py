import os
import random
import typing

import pygame

import helper
import sprites

pygame.init()


def main():
    # D - Display
    screen: pygame.Surface = pygame.display.set_mode((888, 480))
    pygame.display.set_caption("Jetpack Joyride")

    # E - Entities
    dx = 8

    background = sprites.BackgroundSprite(
        screen=screen,
        images=list(next(helper.load_images(os.path.join("assets", "background")))),
        speed=-dx
    )

    player = sprites.Player(screen=screen, position=(round(screen.get_size()[0] * (1 / 8)), 0))
    player.flying = False

    players = pygame.sprite.Group(player)

    zapper_spacing = 500
    zappers = pygame.sprite.Group()

    game_sprites = pygame.sprite.OrderedUpdates(background, zappers, players)

    # A - Assign Variables
    zapper_distance = 0

    clock = pygame.time.Clock()
    keep_going = True

    # Hide the mouse pointer
    pygame.mouse.set_visible(False)

    while keep_going:

        # T - Time
        clock.tick(60)

        # E - Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.flying = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.flying = False

        if zapper_distance > zapper_spacing:
            zapper_distance = 0

            zappers.add(
                sprites.Zapper(
                    screen=screen,
                    velocity=(-dx, 0),
                    position=(screen.get_size()[0] - 2, random.randrange(0, screen.get_size()[1] - 1)),
                    direction=helper.chance(0.5)
                )
            )

            game_sprites.add(zappers)

        zapper_distance += dx
        # R - Refresh Screen
        game_sprites.update()
        game_sprites.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
