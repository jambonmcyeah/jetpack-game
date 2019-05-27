import os
import random
import typing

import pygame

import helper
import sprites

# I - Initialization
pygame.init()


def main():
    # D - Display
    screen: pygame.Surface = pygame.display.set_mode((888, 480))
    pygame.display.set_caption("Jetpack Joyride")

    # E - Entities
    dx = 8

    # Background

    backgrounds = pygame.sprite.Group(
        [
            sprites.BackgroundSprite(
                screen=screen,
                images=list(images),
                speed=0
            )
            for images in helper.load_images(os.path.join("assets", "background"))
        ]
    )

    # Player
    player = sprites.Player(screen=screen, position=(round(screen.get_size()[0] * (1 / 8)), 0))
    player.flying = False

    players = pygame.sprite.Group(player)

    # Zapper
    zapper_spacings = (300, 500)
    zappers = pygame.sprite.Group()

    # Scoreboard
    scoreboard = sprites.Scoreboard()
    scoreboards = pygame.sprite.Group(scoreboard)

    # Groups
    background_sprites = [backgrounds, zappers]
    foreground_sprites = [scoreboards, players]

    all_sprites = [background_sprites, foreground_sprites]
    game_sprites = pygame.sprite.LayeredUpdates(helper.flatten(all_sprites))

    # A - Assign Variables
    next_zapper_spacing = random.randint(*zapper_spacings)
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

        for group in background_sprites:
            for sprite in group:
                if isinstance(sprite, sprites.MovingSprite):
                    sprite.dx = -dx

        background_speed = -dx

        for sprite in reversed(list(backgrounds)):
            sprite.speed = round(background_speed)
            background_speed *= (3 / 4)

        if zapper_distance > next_zapper_spacing:
            zapper_distance = 0

            zappers.add(
                sprites.Zapper.random_spawn(
                    screen=screen,
                    velocity=(-dx, 0),
                )
            )

            next_zapper_spacing = random.randint(*zapper_spacings)

        zapper_distance += dx

        game_sprites.add(helper.flatten(all_sprites))

        for player in pygame.sprite.groupcollide(players, zappers, False, False, pygame.sprite.collide_mask):
            if not player.dead:
                player.dead = True

        if all(map(lambda x: x.dead, players)):
            dx = 0

        scoreboard.pixels += dx

        # R - Refresh Screen
        game_sprites.update()
        game_sprites.draw(screen)

        pygame.display.flip()


if __name__ == '__main__':
    main()
