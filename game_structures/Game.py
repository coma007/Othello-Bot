from game_structures.Board import *


class Game(object):

    def __init__(self, mode, window=None):

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
        self._window = new_window

    def update(self):
        self._board.draw(self._window)
        if self._mode == 2:
            if self._legal_moves is not None:
                self._display_legal_moves()
            pygame.draw.rect(self._window, WHITE, pygame.Rect(0, 700, 700, 30))

    # Prikaz svih dozvoljenih poteza za aktuelnog igrača
    def _display_legal_moves(self):

        for move in self._legal_moves:
            row, col = move
            x = SQUARE_SIZE * col + SQUARE_SIZE // 2
            y = SQUARE_SIZE * row + SQUARE_SIZE // 2
            radius = SQUARE_SIZE // 2 - 10
            pygame.draw.circle(self._window, GREY, (x, y), radius+3)
            pygame.draw.circle(self._window, GREEN1, (x, y), radius)

    # Check if the game is still on
    def game_on(self):
        return len(self._legal_moves) != 0

    # Return winner if the game is over
    def winner(self):
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

    # Change turn from black to white and vice versa
    def _change_turn(self):
        if self._turn == BLACK:
            self._turn = WHITE
        else:
            self._turn = BLACK

    def play(self, row=None, column=None, depth=None, elapsed_time=None):

        if row is not None and column is not None:
            if self._board.insert(row, column, self._turn):

                self._change_turn()
                self._legal_moves = self._board.legal_moves
                self.console()
                print("Black: ", self._board.black)
                print("White: ", self._board.white)
                if depth is not None and elapsed_time is not None:
                    print("Depth: ", depth)
                    print("Elapsed time: ", elapsed_time, " s")
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


    def console(self):
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








