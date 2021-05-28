"""
Modul sa klasom Piece.
"""

try:
    import pygame
except Exception:
    pass
from constants import *


class Piece:
    """
    Klasa Piece modeluje jednu figuricu.
    """

    def __init__(self, row, column, color, mode):
        """
        Konstruktor klase Piece.

        :param row: Red polja na kom je figurica.
        :type row: int
        :param column: Kolona polja na kom je figurica.
        :type column: int
        :param color: Boja figurice.
        :type color: tuple[int, int, int]
        :param mode: Režim igranja.
        :type mode: int
        """

        self._row = row
        self._column = column
        self._color = color

        if mode == 2:
            self._x = 0
            self._y = 0
            self._position()

    def __eq__(self, other):
        if not isinstance(other, Piece):
            return False
        return self._color == other.color and (self._row, self._column) == (other.row, other.column)

    def __str__(self):
        if self._color == WHITE:
            color = "W"
        else:
            color = "B"
        return color

    @property
    def row(self):
        return self._row

    @property
    def column(self):
        return self._column

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, new_color):
        self._color = new_color

    def _position(self):
        """
        Privatna metoda koja se koristi u GUI režimu kako bi izračunala pozicija figurice u prozoru.
        """

        self._x = SQUARE_SIZE * self._column + SQUARE_SIZE // 2
        self._y = SQUARE_SIZE * self._row + SQUARE_SIZE // 2

    def draw_piece(self, window):
        """
        Metoda koja se koristi u GUI režimu kako bi se iscrtala figurica.
        """

        radius = SQUARE_SIZE // 2 - 10
        pygame.draw.circle(window, self._color, (self._x, self._y), radius)
