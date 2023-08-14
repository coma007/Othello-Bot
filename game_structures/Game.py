"""
Module with the Game class.
"""

from game_structures.Board import *


class Game(object):
    """
    The Game class models the entirety of the game.
    """

    def __init__(self, mode, window=None):
        """
        Constructor of the Game class.

        :param mode: Game mode.
        :type mode: int
        :param window: Window.
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
        Method to refresh the game.
        """

        self._board.draw(self._window)
        if self._mode == 2:
            if self._legal_moves is not None:
                self._display_legal_moves()
            pygame.draw.rect(self._window, WHITE, pygame.Rect(0, 700, 700, 30))

    def _display_legal_moves(self):
        """
        Private method used in GUI mode to draw all possible moves in the window.
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
        Method to check if the game is ongoing.

        :return: False if the game is over, True otherwise.
        :rtype: bool
        """

        return len(self._legal_moves) != 0

    def winner(self):
        """
        Method to return the current outcome of the game.

        :return: None if the game is not finished, otherwise the winner.
        :rtype: NoneType, str
        """

        if self.game_on():
            return None
        else:
            self._turn = None
            if self._board.black > self._board.white:
                if self._mode == 1:
                    print("BLACK WON!")
                return "BLACK"
            elif self._board.black == self._board.white:
                if self._mode == 1:
                    print("TIE!")
                return "TIE"
            elif self._board.black < self._board.white:
                if self._mode == 1:
                    print("WHITE WON!")
                return "WHITE"

    def _change_turn(self):
        """
        Private method to change the turn.
        """

        if self._turn == BLACK:
            self._turn = WHITE
        else:
            self._turn = BLACK

    def play(self, row=None, column=None, depth=None, elapsed_time=None):
        """
        Method to make the specified move.

        :param row: Row.
        :type row: int
        :param column: Column.
        :type column: int
        :param depth: Depth at which the best move was calculated if bot_logic is taking its turn.
        :type depth: int
        :param elapsed_time: Duration of the move.
        :type elapsed_time: float

        :return: True if the move is made, False otherwise.
        :rtype: bool
        """

        if row is not None and column is not None:
            if self._board.insert(row, column, self._turn):
                self._change_turn()
                self._legal_moves = self._board.legal_moves
                self.console()
                print("Black:", self._board.black)
                print("White:", self._board.white)
                if depth is not None and elapsed_time is not None:
                    print("Depth:", depth)
                    print("Elapsed time:", elapsed_time, "s")
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
            print("Black:", self._board.black)
            print("White:", self._board.white)
            return True

    def console(self):
        """
        Method to print the current state of the game to the console.
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
