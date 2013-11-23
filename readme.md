## How to run &amp; install

1. Download and install Python 2.7
1. Download and install the latest copy of [PyGame](http://www.pygame.org/news.html)
1. Run `> python main`

## How to play

The game of life has 4 basic rules:

1. Any live cell with fewer than two live neighbors dies, as if caused by under-population
1. Any live cell with two or three live neighbors lives on to the next generation
1. Any live cell with more than three live neighbors dies, as if by overcrowding
1. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction (or resurrection in our case)

### Shape Select Mode
While the game is paused pressing `shift` will enter into shape select mode (the board game will change to a light blue).
In this mode `right + click` any two blocks to draw a box around a particular cell generation. Clicking `save` while in __shape select mode__ will save just the particular region.

While in __shape select mode__ clicking on `load` will load a shape and allow you to drop it anywhere on the screen with a `left + click`

Pressing `middle + click` will clear the __shape select mode__ unloading the chape and clearing the highlight from the screen

## Overview

This is a simple python implementation of the classic __Game of Life__ or __Life__.  Please feel free to experiment
with the code and make any changes.  I do plan to add some more features/functionality in the future.

## Planned Features

- ~~Save entire board~~
- ~~Load board~~
- ~~Save shapes~~
- ~~Load shapes~~
- shape library
- ~~Step through generations~~
- Game grid size
- Better configuration settings (rendering speed mostly)
- ~~Random pattern generation~~


## Bundled with
[Glyphicons.com](http://www.GLYPHICONS.com) - [CC BY](http://creativecommons.org/licenses/by/3.0/)
