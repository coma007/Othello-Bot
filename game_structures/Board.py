"""
Module with the Board class.
"""

from game_structures.Piece import *


class Board(object):
    """
    Class Board models the current state of the board.
    """

    def __init__(self, mode, state=None):
        """
        Constructor of the Board class.

        :param mode: Game mode.
        :type mode: int
        :param state: State on the board.
        :type state: list
        """

        if state is None:
            self._state = []
        else:
            self._state = state

        self._mode = mode
        self._create_pieces()
        self._white = 2
        self._black = 2

        self._legal_moves = []
        self._old_legal_moves = 0
        self._playing = BLACK
        self.all_legal_moves(BLACK)

    def __eq__(self, other):
        return self._state == other.state

    def __str__(self):
        string = "\n    0   1   2   3   4   5   6   7   \n"
        for row in range(ROWS):
            string += f"{row} |"
            for column in range(COLUMNS):
                data = self._state[row][column]
                if data == 0:
                    string += "   |"
                elif data.color == BLACK:
                    string += " X |"
                else:
                    string += " O |"
            string += "\n"
        return string

    @property
    def state(self):
        return self._state

    @property
    def white(self):
        return self._white

    @property
    def black(self):
        return self._black

    @property
    def future_legal_moves(self):
        return self._old_legal_moves

    @property
    def legal_moves(self):
        return self._legal_moves

    @legal_moves.setter
    def legal_moves(self, new_value):
        self._legal_moves = new_value

    @property
    def playing(self):
        return self._playing

    def _create_pieces(self):
        """
        Private method that creates the initial state of the board.
        """

        for i in range(ROWS):
            self._state.append([])
            for j in range(COLUMNS):
                if i in range(3, 5) and j in range(3, 5):
                    if i == j:
                        color = WHITE
                    else:
                        color = BLACK
                    self._state[i].append(Piece(i, j, color, self._mode))
                else:
                    self._state[i].append(0)

    def _draw_fields(self, window):
        """
        Private method used in GUI mode to draw all the squares on the board.

        :param window: Window.
        :type window: pygame.Surface
        """

        if self._mode == 2:
            window.fill(GREEN1)
            for row in range(ROWS):
                for col in range(row % 2, ROWS, 2):
                    pygame.draw.rect(window, GREEN2, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw(self, window):
        """
        Method used in GUI mode to draw all the pieces on the board.

        :param window: Window.
        :type window: pygame.Surface
        """

        self._draw_fields(window)
        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self._state[row][col]
                if piece != 0:
                    piece.draw_piece(window)

    def all_legal_moves(self, color):
        """
        Method that calculates all legal moves for the current state of the board.

        :param color: Color of the player for whom to find legal moves.
        :type color: tuple[int, int, int]
        """

        moves = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self._state[row][col] != 0:
                    continue
                elif self._legal_directions(row, col, color):
                    moves.append((row, col))
        self._old_legal_moves = len(self._legal_moves)
        self._legal_moves = moves

    def _legal_directions(self, row, column, color):
        """
        Private method that calculates all legal moves for the current state of the board in all directions.

        :param row: Row.
        :type row: int
        :param column: Column.
        :type column: int
        :param color: Color of the player for whom to find legal moves.
        :type color: tuple[int, int, int]

        :return: True if a move can be played on the given square, False otherwise.
        :rtype: bool
        """

        north_west = self._legal_one_direction(row, -1, column, -1, color)
        north = self._legal_one_direction(row, -1, column, 0, color)
        north_east = self._legal_one_direction(row, -1, column, 1, color)
        east = self._legal_one_direction(row, 0, column, 1, color)
        south_east = self._legal_one_direction(row, 1, column, 1, color)
        south = self._legal_one_direction(row, 1, column, 0, color)
        south_west = self._legal_one_direction(row, 1, column, -1, color)
        west = self._legal_one_direction(row, 0, column, -1, color)

        if north_west or north or north_east or east or south_east or south or south_west or west:
            return True

    def _legal_one_direction(self, y, dy, x, dx, color):
        """
        Private method that calculates all legal moves for the current state of the board in a single direction.

        :param y: Horizontal position.
        :type y: int
        :param dy: Horizontal shift.
        :type dy: int
        :param x: Vertical position.
        :type x: int
        :param dx: Vertical shift.
        :type dx: int
        :param color: Color of the player for whom to find legal moves.
        :type color: tuple[int, int, int]

        :return: True if a move can be played in the given direction, False otherwise.
        :rtype: bool
        """

        if self._on_edge(x, dx) or self._on_edge(y, dy) or self._on_edge(x, 2*dx) or self._on_edge(y, 2*dy):
            return False
        if self._state[y + dy][x + dx] != 0:
            if self._state[y + dy][x + dx].color == color:
                return False
        if self._state[y + dy][x + dx] == 0:
            return False
        return self._encapsulating_opponent(y + 2 * dy, dy, x + 2 * dx, dx, color)

    def _encapsulating_opponent(self, y, dy, x, dx, color):
        """
        Private method that checks if the opponent is encapsulated by a move.

        :param y: Horizontal position.
        :type y: int
        :param dy: Horizontal shift.
        :type dy: int
        :param x: Vertical position.
        :type x: int
        :param dx: Vertical shift.
        :type dx: int
        :param color: Color of the player for whom to find legal moves.
        :type color: tuple[int, int, int]

        :return: True if the opponent is encapsulated, False otherwise.
        :rtype: bool
        """

        if self._state[y][x] == 0:
            return False
        if self._state[y][x] != 0:
            if self._state[y][x].color == color:
                return True

        if self._on_edge(x, dx) or self._on_edge(y, dy):
            return False

        return self._encapsulating_opponent(y + dy, dy, x + dx, dx, color)

    def _on_edge(self, a, da):
        """
        Private method that checks if a position is near the edges of the board.

        :param a: Position.
        :type a: int
        :param da: Shift.
        :type da: int

        :return: True if the position is near the board edge, False otherwise.
        :rtype: bool
        """

        return a + da < 0 or a + da > 7

    def insert(self, row, column, color):
        """
        Method for inserting a new piece into the current state. If the insertion is successful, the move will be
        played; otherwise, it won't.

        :param row: Row.
        :type row: int
        :param column: Column.
        :type column: int
        :param color: Color of the player for whom to find legal moves.
        :type color: tuple[int, int, int]

        :return: True if the move was played, False otherwise.
        :rtype: bool
        """

        new = Piece(row, column, color, self._mode)
        try:
            field = self._state[row][column]
        except IndexError:
            return False
        if field == 0 and (row, column) in self._legal_moves:
            self._state[row][column] = new
            self._flip_opponent(row, column, color)
            if color == WHITE:
                self._white += 1
                self._playing = BLACK
            else:
                self._black += 1
                self._playing = WHITE
            self.all_legal_moves(self._playing)
            return True
        else:
            return False

    def _flip_opponent(self, row, column, color):
        """
        Private method for flipping opponent's pieces after a move is played.

        :param row: Row.
        :type row: int
        :param column: Column.
        :type column: int
        :param color: Color of the player for whom to find legal moves.
        :type color: tuple[int, int, int]
        """

        self._flip_opponent_line(row, -1, column, -1, color)
        self._flip_opponent_line(row, -1, column, 0, color)
        self._flip_opponent_line(row, -1, column, 1, color)
        self._flip_opponent_line(row, 0, column, 1, color)
        self._flip_opponent_line(row, 1, column, 1, color)
        self._flip_opponent_line(row, 1, column, 0, color)
        self._flip_opponent_line(row, 1, column, -1, color)
        self._flip_opponent_line(row, 0, column, -1, color)

    def _flip_opponent_line(self, y, dy, x, dx, color):
        """
        Private method for flipping opponent's pieces in a single direction after a move is played.

        :param y: Horizontal position.
        :type y: int
        :param dy: Horizontal shift.
        :type dy: int
        :param x: Vertical position.
        :type x: int
        :param dx: Vertical shift.
        :type dx: int
        :param color: Color of the player for whom to find legal moves.
        :type color: tuple[int, int, int]

        :return: True if opponent's pieces were flipped, False otherwise.
        :rtype: bool
        """

        if self._on_edge(x, dx) or self._on_edge(y, dy):
            return False
        if self._state[y + dy][x + dx] == 0:
            return False
        if self._state[y + dy][x + dx].color == color:
            return True

        if self._flip_opponent_line(y + dy, dy, x + dx, dx, color):
            self._state[y + dy][x + dx].color = color
            if color == WHITE:
                self._white += 1
                self._black -= 1
            else:
                self._white -= 1
                self._black += 1
            return True
        else:
            return False
