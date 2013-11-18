"""
author: Mike McMahon
date: 11/17/13
"""

import Tkinter
import tkFileDialog

_root = Tkinter.Tk()
_root.withdraw()
_file_options = {
    'filetypes': [
        ('generation file .gen', '.gen'),
        ('all files', '.*')
    ]
}

def _write_content(filename, content):
    try:
        with open(filename, 'wb') as game_file:
            game_file.write(content)
    except IOError:
        return False

    return True

def _read_content(filename):
    try:
        with open(filename, 'rb') as game_file:
            content = ''
            for row in game_file:
                content += row.rstrip()
            return content
    except IOError:
        return False


def _save_file(initialfile=''):
    _file_options['initialfile'] = initialfile
    return tkFileDialog.asksaveasfilename(**_file_options)

def _load_file(initialfile=''):
    _file_options['initialfile'] = initialfile
    return tkFileDialog.askopenfilename(**_file_options)

def save_generation(collected_board):
    filename = _save_file('generation.gen')
    return _write_content(filename, collected_board)

def load_generation():
    filename = _load_file('generation.gen')
    return _read_content(filename)