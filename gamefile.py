"""
author: Mike McMahon

created: 11/13/13

"""

import Tkinter
import tkFileDialog


class _FileHandler:
    pass

_root = _FileHandler()
_root.windower = Tkinter.Tk()
_root.windower.withdraw()
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


def _init():
    _root.windower = Tkinter.Tk()
    _root.windower.withdraw()


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
    _init()
    _file_options['initialfile'] = initialfile
    filename = tkFileDialog.asksaveasfilename(**_file_options)
    _root.windower.destroy()
    _root.windower.quit()
    return filename


def _load_file(initialfile=''):
    _init()
    _file_options['initialfile'] = initialfile
    filename = tkFileDialog.askopenfilename(**_file_options)
    _root.windower.destroy()
    _root.windower.quit()
    return filename


def save_generation(collected_board):
    filename = _save_file('generation.gen')
    return _write_content(filename, collected_board)


def load_generation():
    filename = _load_file('generation.gen')
    return _read_content(filename)