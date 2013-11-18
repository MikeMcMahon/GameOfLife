"""
author: Family
date: 11/17/13
"""

import os

def collect_gameboard(cells, rows, cols):
    collected = ''
    for row in range(rows):
        for col in range(cols):
            collected += '1' if cells[(cols * row) + col].is_cell_alive() else '0'
        collected += os.linesep
    return collected