"""
author: Mike McMahon
 
created: 11/13/13
 
"""
from decimal import Decimal
import sys
import pygame

from pygame.locals import *

from colors import WHITE, BLACK
from physics import collision_detection
from sprites import Cell


def main():
    size = width, height = 320, 240

    screen = pygame.display.set_mode(size)

    pygame.font.init()
    default_font = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(default_font, 15)

    start = font_renderer.render("Start", 1, BLACK)
    clear = font_renderer.render("Clear", 1, BLACK)

    is_paused = True

    cols, rows = 25, 25
    cell_size = (10, 10)
    cell_padding = 1

    game_sprites = [Cell(0, 0, *cell_size) for x in xrange(rows * cols)]

    sprite_renderer = pygame.sprite.RenderPlain(game_sprites)

    run_y = 20
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
                mouse_loc = pygame.mouse.get_pos()
                if collision_detection(start_loc, mouse_loc):
                    start = font_renderer.render("Pause" if is_paused else "Start", 1, BLACK)
                    is_paused = not is_paused

                if is_paused:
                    # Clears out the game board
                    if collision_detection(clear_loc, mouse_loc):
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
        screen.fill(WHITE)
        start_loc = screen.blit(start, (5, 5))
        clear_loc = screen.blit(clear, (screen.get_width() - clear.get_width() - 5,  5))

        sprite_renderer.draw(screen)

        pygame.display.flip()

pygame.init()
main()