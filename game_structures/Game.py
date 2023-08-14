"""
Modul sa klasom Game.
"""

from game_structures.Board import *


class Game(object):
    """
    Klasa Game modeluje cjelinu igre.
    """

    def __init__(self, mode, window=None):
        """
        Konstruktor klase Game.

        :param mode: Režim igranja.
        :type mode: int
        :param window: Prozor.
        :type window: pygame.Surface
        """

        self._window = window
        self._mode = mode
        self._board = Board(self._mode)

        self._turn = BLACK
        self._legal_moves = self._board.legal_moves

        self.play()

    @property
    def board(self):
        return self._board

    @property
    def black(self):
        return self._board.black

    @property
    def white(self):
        return self._board.white

    @property
    def turn(self):
        return self._turn

    @property
    def window(self):
        return self._window

    @window.setter
    def window(self, new_window):
        """
        :type new_window: pygame.Surface
        """
        self._window = new_window

    def update(self):
        """
        Metoda za osvježavanje igre.
        """

        self._board.draw(self._window)
        if self._mode == 2:
            if self._legal_moves is not None:
                self._display_legal_moves()
            pygame.draw.rect(self._window, WHITE, pygame.Rect(0, 700, 700, 30))

    def _display_legal_moves(self):
        """
        Privatna metoda koja se koristi u GUI režimu kako bi se u prozoru iscrtali svi mogući potezi.
        """

        for move in self._legal_moves:
            row, col = move
            x = SQUARE_SIZE * col + SQUARE_SIZE // 2
            y = SQUARE_SIZE * row + SQUARE_SIZE // 2
            radius = SQUARE_SIZE // 2 - 10
            pygame.draw.circle(self._window, GREY, (x, y), radius+3)
            pygame.draw.circle(self._window, GREEN1, (x, y), radius)

    def game_on(self):
        """
        Metoda koja provjerava da li je igra gotova.

        :return: False ukoliko je igra gotova, u suprotnom True.
        :rtype: bool
        """

        return len(self._legal_moves) != 0

    def winner(self):
        """
        Metoda koja vraća trenutni ishod igre.

        :return: None ukoliko igra nije završena, u suprotnom pobjednika.
        :rtype: NoneType, str
        """

        if self.game_on():
            return None
        else:
            self._turn = None
            if self._board.black > self._board.white:
                if self._mode == 1:
                    print("BLACK WON !")
                return "BLACK"
            elif self._board.black == self._board.white:
                if self._mode == 1:
                    print("TIE !")
                return "TIE"
            elif self._board.black < self._board.white:
                if self._mode == 1:
                    print("WHITE WON !")
                return "WHITE"

    def _change_turn(self):
        """
        Privatna metoda kojom se mijenja potez.
        """

        if self._turn == BLACK:
            self._turn = WHITE
        else:
            self._turn = BLACK

    def play(self, row=None, column=None, depth=None, elapsed_time=None):
        """
        Metoda koja odigra zadani potez.

        :param row: Red.
        :type row: int
        :param column: Kolona.
        :type column: int
        :param depth: Dubina na kojoj se računao najbolji potez ukoliko je na potezu bot_logic.
        :type depth: int
        :param elapsed_time: Trajanje poteza.
        :type elapsed_time: float

        :return: True ukoliko je potez odigran, u suprotnom False.
        :rtype: bool
        """

        if row is not None and column is not None:
            if self._board.insert(row, column, self._turn):
                self._change_turn()
                self._legal_moves = self._board.legal_moves
                self.console()
                print("Black: ", self._board.black)
                print("White: ", self._board.white)
                if depth is not None and elapsed_time is not None:
                    print("Depth: ", depth)
                    print("Elapsed time: ", elapsed_time, "s")
                if len(self._legal_moves) != 0:
                    if self._board.playing == BLACK:
                        print("\nBlack's turn...")
                    else:
                        print("\nWhite's turn...")
                return True
            else:
                return False
        else:
            print("\n\nBlack's turn...")
            self.console()
            print("Black: ", self._board.black)
            print("White: ", self._board.white)
            return True

    def console(self):
        """
        Metoda koja u konzoli ispisuje trenutno stanje igre.
        """

        print("\n    0   1   2   3   4   5   6   7   ")
        for row in range(ROWS):
            print(f"{row} |", end="")
            for column in range(COLUMNS):
                hint = (row, column) in self._legal_moves
                data = self._board.state[row][column]
                if hint and data == 0:
                    print(" + ", end="|")
                elif data == 0 and not hint:
                    print("   ", end="|")
                elif data.color == BLACK:
                    print(" X ", end="|")
                else:
                    print(" O ", end="|")
            print("")
