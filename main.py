"""
author: Mike McMahon
 
created: 11/13/13
 
"""
import sys
import pygame

from pygame.locals import *

from colors import WHITE, BLACK
from physics import collision_detection
from sprites import Citizen


def main():
    size = width, height = 320, 240

    screen = pygame.display.set_mode(size)

    pygame.font.init()
    default_font = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(default_font, 15)

    start = font_renderer.render("Start", 1, BLACK)
    clear = font_renderer.render("Clear", 1, BLACK)

    is_paused = True

    cols, rows = 17, 17
    citizen_size = (10, 10)
    game_grid = [[0 for x in xrange(rows)] for x in xrange(cols)]

    sprite_renderer = pygame.sprite.RenderPlain()

    run_y = 20
    for row in range(rows):
        run_x = (screen.get_width() / 2) - ((cols * 13) / 2)
        for col in range(cols):
            sprite = Citizen(run_x, run_y, *citizen_size)
            sprite_renderer.add(sprite)
            game_grid[row][col] = sprite
            run_x += 11
        run_y += 11

    game_ticks = pygame.time.get_ticks()
    game_ticks_elapsed = 0
    game_ticks_fps = 120

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
                            sprite.update()

                    # If the game is paused and we hover over the game piece???
                    for sprite in sprite_renderer.sprites():
                        if collision_detection(sprite.get_rect(), mouse_loc):
                            sprite.kill() if sprite.citizen_alive() else sprite.resurrect()
                            sprite.update()

        if is_paused:
            mouse_loc = pygame.mouse.get_pos()
            # Check for any collisions
            for sprite in sprite_renderer.sprites():
                if collision_detection(sprite.get_rect(), mouse_loc):
                    sprite.highlight()
                else:
                    sprite.clear_highlight()

                sprite.update()

        if game_ticks_elapsed - game_ticks >= game_ticks_fps:
            game_ticks = game_ticks_elapsed

            if not is_paused:
                # GAME LOGIC GOES HERE
                # Conways game of life rules
                # 1) Any live cell with fewer than two live neighbors dies (under-population)
                # 2) Any live cell with two or three live neighbors lives on to the next generation
                # 3) Any live cell with more than three live neighbors dies as if by overcrowding
                # 4) Any dead cell with exactly three live neighbors becomes a live cell as if by reproduction
                for row in range(rows):
                    for col in range(cols):
                        # surrounding positions are
                        # [ row-1,col-1, row-1,col, row-1,col+1 ]
                        # [ row,col-1,   SELF,      row,col+1 ]
                        # [ row+1,col-1, row+1,col, row+1,col+1 ]
                        neighbors = [(row-1, col-1), (row-1, col), (row-1, col+1),
                                     (row, col-1), (row, col+1),
                                     (row+1, col-1), (row+1, col), (row+1, col+1)]

                        alive_neighbors = 0
                        for neighbor in neighbors:
                            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                                if game_grid[neighbor[0]][neighbor[1]].citizen_alive():
                                    alive_neighbors += 1
                        if game_grid[row][col].citizen_alive():
                            if alive_neighbors < 2:
                                game_grid[row][col].kill_next_generation()
                                game_grid[row][col].update()
                            if 2 <= alive_neighbors <= 3:
                                # Keep alive
                                pass
                            if alive_neighbors > 3:
                                game_grid[row][col].kill_next_generation()
                                game_grid[row][col].update()
                        else:
                            if alive_neighbors == 3:
                                game_grid[row][col].resurrect_next_generation()
                                game_grid[row][col].update()

                for row in range(rows):
                    for col in range(cols):
                        game_grid[row][col].generate()

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