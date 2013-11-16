"""
author: Mike McMahon
 
created: 11/13/13
 
"""
from decimal import Decimal
import random
import sys
import pygame

from pygame.locals import *

from colors import *
from physics import collision_detection
from sprites import Cell, GameFont

import font


def main():
    size = width, height = 320, 320

    screen = pygame.display.set_mode(size)

    default_font, font_renderer = font.init()

    start = GameFont(
        font_renderer,
        "Start",
        "glyphicons_173_play.png"
    )
    start.set_pos(5, 5)

    clear_screen = GameFont(
        font_renderer,
        "Clear",
        "glyphicons_067_cleaning.png"
    )
    clear_screen.set_pos(
        (screen.get_width() - clear_screen.get_width() - 5),
        5
    )

    random_seed = GameFont(
        font_renderer,
        "Random",
        "glyphicons_009_magic.png"
    )
    random_seed.set_pos(
        (screen.get_width() / 2) - random_seed.get_width() / 2,
        5
    )

    is_paused = True

    cols, rows = 25, 25
    cell_size = (10, 10)
    cell_padding = 1

    game_sprites = [Cell(0, 0, *cell_size) for x in xrange(rows * cols)]

    font_sprite_renderer = pygame.sprite.RenderPlain(start, random_seed, clear_screen)
    sprite_renderer = pygame.sprite.RenderPlain(game_sprites)

    run_y = 27
    for row in range(rows):
        run_x = (Decimal(screen.get_width()) / Decimal(2)) - (Decimal(cols * (cell_size[0] + cell_padding)) / Decimal(2))
        for col in range(cols):
            index = (cols * row) + col
            neighbors = [
                # The following ensures our bounds are within the visual graph
                (((row-1) * cols) + col-1) if row - 1 >= 0 and col - 1 >= 0 else -1,
                (((row-1) * cols) + col) if row - 1 >= 0 else -1,
                (((row-1) * cols) + col+1) if row - 1 >= 0 and col + 1 < cols else -1,
                ((row * cols) + col-1) if col - 1 >= 0 else -1,
                ((row * cols) + col+1) if col + 1 < cols else -1,
                (((row+1) * cols) + col-1) if row + 1 < rows and col - 1 >= 0 else -1,
                (((row+1) * cols) + col) if row + 1 < rows else -1,
                (((row+1) * cols) + col+1) if row + 1 < rows and col + 1 < cols else -1,
            ]

            game_sprites[index].set_pos(run_x, run_y)

            for neighbor in neighbors:
                if neighbor >= 0:
                    # Builds the graph of game sprites (or at least, what sprites we can navigate to from this one
                    game_sprites[index].add_neighbor(game_sprites[neighbor])

            run_x += cell_size[0] + cell_padding
        run_y += cell_size[1] + cell_padding

    game_ticks = pygame.time.get_ticks()
    game_ticks_elapsed = 0
    game_ticks_fps = 120

    last_highlighted = Cell(0, 0, 0, 0)
    while True:
        # HANDLES THE INPUT
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pressed = pygame.mouse.get_pressed()
                if pressed[0] == 0:
                    continue
                mouse_loc = pygame.mouse.get_pos()
                if collision_detection(start.get_rect(), mouse_loc):
                    args = ("Pause", "glyphicons_174_pause.png") if is_paused else ("Start", "glyphicons_173_play.png")
                    start.update(args)
                    is_paused = not is_paused

                if is_paused:
                    if collision_detection(random_seed.get_rect(), mouse_loc):
                        for sprite in sprite_renderer.sprites():
                            if random.randint(0, 1) == 0:
                                sprite.resurrect()
                            else:
                                sprite.kill()

                    # Clears out the game board
                    if collision_detection(clear_screen.get_rect(), mouse_loc):
                        for sprite in sprite_renderer.sprites():
                            sprite.kill()

                    # If the game is paused and we hover over the game piece???
                    for sprite in sprite_renderer.sprites():
                        if collision_detection(sprite.get_rect(), mouse_loc):
                            sprite.kill() if sprite.is_cell_alive() else sprite.resurrect()
                    sprite_renderer.update(True, False, True)

        if is_paused:
            mouse_loc = pygame.mouse.get_pos()
            # Check for any collisions

            hit_none = True
            for sprite in sprite_renderer.sprites():
                if collision_detection(sprite.get_rect(), mouse_loc):
                    hit_none = False
                    if not sprite == last_highlighted:
                        last_highlighted.clear_highlight(True)
                        last_highlighted = sprite
                    sprite.highlight()
                else:
                    sprite.clear_highlight()
            if hit_none:
                last_highlighted.clear_highlight(True)

            sprite_renderer.update(True, False, True)

        if game_ticks_elapsed - game_ticks >= game_ticks_fps and not is_paused:
            game_ticks = game_ticks_elapsed

            sprite_renderer.update(False, False, False)
            sprite_renderer.update(False, True, True)

        else:
            game_ticks_elapsed = pygame.time.get_ticks()

        # RENDER LOGIC GOES PAST THIS POINT
        fill_gradient(screen, WHITE, GREY)
        font_sprite_renderer.update()
        font_sprite_renderer.draw(screen)
        sprite_renderer.draw(screen)

        pygame.display.flip()

pygame.init()
main()