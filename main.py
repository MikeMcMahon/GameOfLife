"""
author: Mike McMahon
 
created: 11/13/13
 
"""
from decimal import Decimal
import random
import sys

from pygame.locals import *
import board

from colors import *
import gamefile
from physics import collision_detection
from sprites import Cell, GameButton

import font


def main():

    default_font, gamefont = font.init(13)

    start = GameButton(gamefont, "Start", "glyphicons_173_play.png")
    random_seed = GameButton(gamefont, "Random", "glyphicons_009_magic.png")
    clear_screen = GameButton(gamefont, "Clear", "glyphicons_067_cleaning.png")
    load_generation = GameButton(gamefont, "Load", "glyphicons_144_folder_open.png")
    save_generation = GameButton(gamefont, "Save", "glyphicons_446_floppy_save.png")
    step_generation = GameButton(gamefont, "Step", "glyphicons_178_step_forward.png")
    game_settings = GameButton(gamefont, "Settings", "glyphicons_280_settings.png")

    cols, rows = 25, 25
    cell_size = (10, 10)
    cell_padding = 1
    size = width, height = 320, ((start.get_height()) * 2) + (rows * (cell_size[1] + cell_padding)) + 20
    screen = pygame.display.set_mode(size)

    load_generation.set_pos(
        save_generation.get_width() + 10,
        screen.get_height() - load_generation.get_height() - 5,
    )
    save_generation.set_pos(
        5,
        screen.get_height() - save_generation.get_height() - 5,
    )
    start.set_pos(5, 5)
    step_generation.set_pos(
        start.get_pos()[0] + start.get_width() + 5,
        5,
    )
    random_seed.set_pos(
        (step_generation.get_pos()[0] + step_generation.get_width() + 5),
        5
    )
    clear_screen.set_pos(
        (random_seed.get_pos()[0] + random_seed.get_width() + 5),
        5
    )
    game_settings.set_pos(
        screen.get_width() - game_settings.get_width() - 5,
        screen.get_height() - game_settings.get_height() - 5
    )

    game_state = board.GameState()

    def start_clicked():
        if not game_state.is_shape_select:
            paused = game_state.is_paused
            args = ("Stop", "glyphicons_174_pause.png") if paused else ("Start", "glyphicons_173_play.png")
            start.set_label(args[0])
            start.set_icon(args[1])
            game_state.is_paused = not game_state.is_paused
        elif game_state.is_shape_select:
            start.set_label("Start")
            start.set_icon("glyphicons_173_play.png")
            game_state.is_paused = True
            game_state.is_shape_load = False
            game_state.is_shape_select = False
            shape_select.clear()
            shape_select.clear_loaded()
            for sprite in game_sprites:
                sprite.background_color = LIGHT_BLUE if game_state.is_shape_select else GREY
        return start_clicked

    def random_clicked():
        if game_state.is_paused and not game_state.is_shape_select:
            for sprite in sprite_renderer.sprites():
                if random.randint(0, 100) <= 50:
                    sprite.resurrect()
                else:
                    sprite.kill()
        return random_clicked

    def clear_clicked():
        if game_state.is_paused:
            for sprite in sprite_renderer.sprites():
                if game_state.is_shape_select and not game_state.is_shape_load:
                    sprite.is_shape_selected = False
                    sprite.clear_highlight(True)
                    shape_select.clear()
                else:
                    sprite.kill()
        return clear_clicked

    def save_gameboard_clicked():
        if game_state.is_paused:
            if not game_state.is_shape_select:
                gamefile.save_generation(board.collect_gameboard(game_sprites, rows, cols))
            else:
                gamefile.save_shape(board.collect_gameboard(*shape_select.get_selected(rows, game_sprites)))
        return save_gameboard_clicked

    def load_gameboard_clicked():
        if game_state.is_paused:
            if not game_state.is_shape_select:
                new_board = gamefile.load_generation()
                if not new_board:
                    pass  # TODO - show a dialog that we failed...
                else:
                    for i in range(len(new_board)):
                        if new_board[i] == '0':
                            game_sprites[i].kill()
                        elif new_board[i] == '1':
                            game_sprites[i].resurrect()
            else:
                game_shape = gamefile.load_shape()
                if not game_shape:
                    pass
                else:
                    shape_select.read_shape_data(game_shape)
                    game_state.is_shape_load = True

        return load_gameboard_clicked

    def step_generation_clicked():
        if game_state.is_paused and not game_state.is_shape_select:
            sprite_renderer.update(False, False, False)
            sprite_renderer.update(False, True, True)
        return step_generation_clicked

    clear_screen.on_clicked(clear_clicked)
    random_seed.on_clicked(random_clicked)
    start.on_clicked(start_clicked)
    save_generation.on_clicked(save_gameboard_clicked)
    load_generation.on_clicked(load_gameboard_clicked)
    step_generation.on_clicked(step_generation_clicked)

    game_sprites = [Cell(0, 0, *cell_size) for x in xrange(rows * cols)]
    for sprite in game_sprites:
        sprite.alive_color = GREEN

    font_sprite_renderer = pygame.sprite.RenderPlain(
        start,
        random_seed,
        clear_screen,
        save_generation,
        load_generation,
        step_generation,
        game_settings
    )

    sprite_renderer = pygame.sprite.RenderPlain(game_sprites)

    run_y = (5 * 2) + (clear_screen.get_height() * 1)
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
    shape_select = board.ShapeSelect()
    while True:
        # HANDLES THE INPUT
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == KEYDOWN:
                if pygame.key.get_mods() & KMOD_SHIFT and game_state.is_paused:
                    game_state.is_shape_select = not game_state.is_shape_select
                    if game_state.is_shape_load:
                        game_state.is_shape_load = False
                        shape_select.clear_loaded()
                    if not game_state.is_shape_select:
                        start.set_icon("glyphicons_173_play.png")
                        start.set_label("Start")
                        load_generation.set_label("Load")
                        shape_select.clear()
                        shape_select.highlight_selected(cols, game_sprites)
                    else:
                        start.set_icon("glyphicons_099_vector_path_all.png")
                        start.set_label("Shpe")
                        load_generation.set_label("Load Shape")
                    for sprite in game_sprites:
                        sprite.background_color = LIGHT_BLUE if game_state.is_shape_select else GREY

            if event.type == MOUSEBUTTONDOWN:
                mouse_left, mouse_middle, mouse_right = pressed = pygame.mouse.get_pressed()
                mouse_loc = pygame.mouse.get_pos()
                font_sprite_renderer.update(mouse_loc, pressed)

                if game_state.is_paused:
                    if mouse_middle == 1 and game_state.is_shape_load and game_state.is_shape_select:
                        game_state.is_shape_load = False
                        shape_select.clear()
                        shape_select.highlight_selected(cols, game_sprites)

                    if mouse_right == 1 and game_state.is_shape_select:
                        #  Ugh - use a directed graph at some point stored based on direction (path finding much)
                        for row in range(rows):
                            for col in range(cols):
                                # Put us in shape select mode
                                if collision_detection(game_sprites[(cols * row) + col].get_rect(), mouse_loc):
                                    pos = (row, col)
                                    # Stores and clears coords for determining the shape dimensions
                                    if shape_select.first == pos:
                                        shape_select.clear_first()
                                        shape_select.highlight_selected(cols, game_sprites)
                                    elif shape_select.last == pos:
                                        shape_select.clear_last()
                                        shape_select.highlight_selected(cols, game_sprites)
                                    elif shape_select.first == (-1, -1):
                                        shape_select.first = pos
                                        shape_select.highlight_selected(cols, game_sprites)
                                    else:
                                        # Allows the final point to be reset so the box can be easily re-sized
                                        shape_select.last = pos
                                        shape_select.highlight_selected(cols, game_sprites)

                    if mouse_left == 1:
                        if game_state.is_shape_select and game_state.is_shape_load:
                            for row in range(rows):
                                for col in range(cols):
                                    if collision_detection(game_sprites[(cols * row) + col].get_rect(), mouse_loc):
                                        shape_select.drop_shape(rows, cols, (col, row), game_sprites)
                        elif not game_state.is_shape_load:
                            # Resurrect / kill sprites on click!
                            for sprite in sprite_renderer.sprites():
                                if collision_detection(sprite.get_rect(), mouse_loc):
                                    sprite.kill() if sprite.is_cell_alive() else sprite.resurrect()

                    sprite_renderer.update(True, False, True)

        mouse_loc = pygame.mouse.get_pos()
        font_sprite_renderer.update(mouse_loc, (0, 0, 0, 0))
        if game_state.is_paused:
            hit_none = True
            # Only clear this when we are in a drag/drop mode
            if game_state.is_shape_load and game_state.is_shape_select:
                for sprite in game_sprites:
                    sprite.is_shape_selected = False
            for row in range(rows):
                for col in range(cols):
                    # Put us in shape select mode
                    index = (cols * row) + col
                    if collision_detection(game_sprites[index].get_rect(), mouse_loc):
                        if game_state.is_shape_load and game_state.is_shape_select:
                            shape_select.drop_shape(rows, cols, (col, row), game_sprites, highlight=True)
                        else:
                            hit_none = False
                            if not game_sprites[index] == last_highlighted:
                                last_highlighted.clear_highlight(True)
                                last_highlighted = game_sprites[index]
                            game_sprites[index].highlight()
                    else:
                        game_sprites[index].clear_highlight()
            if hit_none:
                last_highlighted.clear_highlight(True)

            sprite_renderer.update(True, False, True)

        if game_ticks_elapsed - game_ticks >= game_ticks_fps and not game_state.is_paused:
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