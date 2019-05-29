""" Author: Jun Bo Bi
    Date: May 29, 2019
    Desc: Jetpack Joyride Game
"""

import os
import random

import pygame

import helper
import sprites

# I - Initialization
pygame.init()


def main():
    """This function defines the mainline logic for this program"""

    # D - Display
    screen: pygame.Surface = pygame.display.set_mode((1000, 480))
    pygame.display.set_caption("Jetpack Joyride")

    # E - Entities

    # Music
    pygame.mixer.music.load(os.path.join("assets", "audio", "music.wav"))
    pygame.mixer.music.play(-1)

    # Speed
    dx = 8

    # Background

    backgrounds = pygame.sprite.Group(
        sprites.BackgroundSprite(screen=screen, images=list(images), velocity=(0, 0))
        for images in helper.load_images(os.path.join("assets", "background"))
    )

    # Players
    player = sprites.Player(screen=screen, position=(round(screen.get_size()[0] * (1 / 8)), 0))
    player.flying = False

    players = pygame.sprite.Group(player)

    # Zappers
    zapper_spacings = (300, 500)
    zappers = pygame.sprite.Group()

    # Scoreboards
    scoreboard = sprites.Scoreboard()
    scoreboards = pygame.sprite.Group(scoreboard)

    # Game Over
    game_over = sprites.TextSprite(
        position=(0, 0),
        font=helper.default_font(48, bold=True),
        text="GAME OVER!",
        color=pygame.Color(255, 255, 255, 255),
        antialias=True
    )

    game_over.horizontally_center(0, screen.get_size()[0])
    game_over.vertically_center(0, screen.get_size()[1])

    # Groups
    background_sprites = [backgrounds, zappers]
    foreground_sprites = [players, scoreboards]

    all_sprites = [background_sprites, foreground_sprites]
    game_sprites = pygame.sprite.LayeredUpdates(all_sprites)

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
                if event.key == pygame.K_SPACE:
                    player.flying = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player.flying = False

        # Update speed of background sprites
        for group in background_sprites:
            for sprite in group:
                if isinstance(sprite, sprites.MovingSprite):
                    sprite.dx = -dx

        background_speed = -dx

        # Update speed of backgrounds
        for sprite in reversed(list(backgrounds)):
            background_speed *= (3 / 4)
            sprite.dx = round(background_speed)

        # Spawn Zapper
        if zapper_distance > next_zapper_spacing:
            zapper_distance = 0

            zappers.add(sprites.Zapper.random_spawn(screen=screen, velocity=(-dx, 0), ))

            next_zapper_spacing = random.randint(*zapper_spacings)

        zapper_distance += dx

        # Add new sprites
        game_sprites.add(all_sprites)

        # Check collisions
        # Optimize precise collisions by only checking them if rect collides
        for player, collided_zappers in pygame.sprite.groupcollide(players, zappers, False, False).items():
            for zapper in collided_zappers:
                if pygame.sprite.collide_mask(player, zapper):
                    if not player.dead:
                        player.dead = True

        # Check if all players are dead
        if all(map(lambda x: x.dead, players)):
            dx = 0
            pygame.mixer.music.stop()
            game_sprites.add(game_over)

        # Update Scoreboard
        scoreboard.pixels += dx

        # R - Refresh Screen
        game_sprites.update()
        game_sprites.draw(screen)

        pygame.display.flip()

    pygame.mouse.set_visible(True)
    pygame.quit()


if __name__ == '__main__':
    main()
