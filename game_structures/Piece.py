try:
    import pygame
except:
    pass
from constants import *


class Piece:

    def __init__(self, row, col, color, mode):
        # Pozicija figurice na tabli
        self._row = row
        self._col = col
        self._color = color

        if mode == 2:
            # Pozicija figurice u prozoru (GUI)
            self._x = 0
            self._y = 0
            self._position()

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self._color == other.color and (self._row, self._col) == (other.row, other.col)

    @property
    def color(self):
        return self._color

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def __str__(self):
        if self._color == WHITE:
            color = "W"
        else:
            color = "B"
        return color

    def _position(self):
        self._x = SQUARE_SIZE * self._col + SQUARE_SIZE // 2
        self._y = SQUARE_SIZE * self._row + SQUARE_SIZE // 2

    def draw_piece(self, window):
        radius = SQUARE_SIZE // 2 - 10
        pygame.draw.circle(window, self._color, (self._x, self._y), radius)


