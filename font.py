"""
author: Mike McMahon

created: 11/15/13
 
"""

import pygame

from colors import BLACK


def init():
    pygame.font.init()
    default_font = pygame.font.get_default_font()
    font_renderer = pygame.font.Font(default_font, 15)

    return default_font, font_renderer


def create_label(font_renderer, label, color=BLACK):
    return font_renderer.render(label, 1, color)


def blit_font(label, surface, *pos):
    return surface.blit(label, pos)