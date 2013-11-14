"""
author: Mike McMahon
 
created: 11/13/13
 
"""
import sys
import pygame
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
    game_grid = [[None for x in xrange(rows)] for x in xrange(cols)]  # ten by ten grid of 10 pixel blocks

    run_y = 20
    for row in range(rows):
        run_x = (screen.get_width() / 2) - ((cols * 13) / 2)
        for col in range(cols):
            game_grid[row][col] = Citizen(run_x, run_y, *citizen_size)
            run_x += 11
        run_y += 11

    game_ticks = pygame.time.get_ticks()
    game_ticks_elapsed = 0
    game_ticks_fps = 120

    while True:
        # HANDLES THE INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_loc = pygame.mouse.get_pos()
                if collision_detection(start_loc, mouse_loc):
                    start = font_renderer.render("Pause" if is_paused else "Start", 1, BLACK)
                    is_paused = not is_paused

                if is_paused:
                    # Clears out the game board
                    if collision_detection(clear_loc, mouse_loc):
                        for row in range(rows):
                            for col in range(cols):
                                game_grid[row][col].kill()
                                #game_grid[row][col].is_highlighted = False

                    # If the game is paused and we hover over the game piece???
                    for row in range(rows):
                        for col in range(cols):
                            if collision_detection(game_grid[row][col].get_rect(), mouse_loc):
                                game_grid[row][col].kill() \
                                    if game_grid[row][col].is_alive() else game_grid[row][col].resurrect()

        if is_paused:
            mouse_loc = pygame.mouse.get_pos()
            # Check for any collisions
            for row in range(rows):
                for col in range(cols):
                    if collision_detection(game_grid[row][col].get_rect(), mouse_loc):
                        game_grid[row][col].highlight()
                    else:
                        game_grid[row][col].clear_highlight()

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
                                if game_grid[neighbor[0]][neighbor[1]].is_alive():
                                    alive_neighbors += 1
                        if game_grid[row][col].is_alive():
                            if alive_neighbors < 2:
                                game_grid[row][col].kill_next_generation()
                            if 2 <= alive_neighbors <= 3:
                                # Keep alive
                                pass
                            if alive_neighbors > 3:
                                game_grid[row][col].kill_next_generation()
                        else:
                            if alive_neighbors == 3:
                                game_grid[row][col].resurrect_next_generation()

            # RENDER LOGIC GOES PAST THIS POINT
            screen.fill(WHITE)
            start_loc = screen.blit(start, (5, 5))
            clear_loc = screen.blit(clear, (screen.get_width() - clear.get_width() - 5,  5))

        else:
            game_ticks_elapsed = pygame.time.get_ticks()

        for row in range(rows):
            for col in range(cols):
                game_grid[row][col].generate()
                game_grid[row][col].blit_to(screen)
        pygame.display.flip()

pygame.init()
main()