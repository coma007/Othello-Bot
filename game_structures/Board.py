from game_structures.Piece import *


class Board(object):

    def __init__(self, board=None):
        if board is None:
            self._board = []

        self._old_legal_moves = 0
        self._legal_moves = []
        self._create_pieces()
        self._white = self._black = 2
        self._playing = BLACK
        self._last = (0,0)

        self.all_legal_moves(BLACK)

    @property
    def board(self):
        return self._board

    @property
    def white(self):
        return self._white

    @property
    def black(self):
        return self._black

    @property
    def old_legal_moves(self):
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

    @property
    def last(self):
        return self._last

    # Initial 4 pieces
    def _create_pieces(self):
        for i in range(ROWS):
            self._board.append([])
            for j in range(COLUMNS):
                if i in range(3, 5) and j in range(3, 5):
                    if i == j:
                        color = WHITE
                    else:
                        color = BLACK
                    self._board[i].append(Piece(i, j, color))
                else:
                    self._board[i].append(0)

    # Drawing only fields
    def _draw_fields(self, window):
        window.fill(GREEN1)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, GREEN2, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # Drawing pieces on fields
    def draw(self, window):
        self._draw_fields(window)
        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self._board[row][col]
                if piece != 0:
                    piece.draw_piece(window)

    # Capture all legal moves
    def all_legal_moves(self, color):

        moves = []
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self._board[row][col] != 0:
                    continue
                elif self._legal_move(row, col, color):
                    moves.append((row, col))
        self._old_legal_moves = len(self._legal_moves)
        self._legal_moves = moves

    # See if the move is legal in all directions
    def _legal_move(self, row, column, color):

        north_west = self._can_move(row, -1, column, -1, color)
        north = self._can_move(row, -1, column, 0, color)
        north_east = self._can_move(row, -1, column, 1, color)
        east = self._can_move(row, 0, column, 1, color)
        south_east = self._can_move(row, 1, column, 1, color)
        south = self._can_move(row, 1, column, 0, color)
        south_west = self._can_move(row, 1, column, -1, color)
        west = self._can_move(row, 0, column, -1, color)

        if north_west or north or north_east or east or south_east or south or south_west or west:
            return True

    # See if the move is legal in certain direction
    def _can_move(self, y, dy, x, dx, color):

        if self._on_edge(x, dx) or self._on_edge(y, dy) or self._on_edge(x, 2*dx) or self._on_edge(y, 2*dy):
            return False
        if self._board[y + dy][x + dx] != 0:
            if self._board[y + dy][x + dx].color == color:
                return False
        if self._board[y + dy][x + dx] == 0:
            return False
        return self._color_match(y + 2 * dy, dy, x + 2 * dx, dx, color)

    # Check if the field is on the edge (or near edge depending on da)
    def _on_edge(self, a, da):
        return a + da < 0 or a + da > 7

    # Check if any pieces would be encapsulated with move, i.e. is the move valid
    def _color_match(self, y, dy, x, dx, color):

        if self._board[y][x] == 0:
            return False
        if self._board[y][x] != 0:
            if self._board[y][x].color == color:
                return True

        if self._on_edge(x, dx) or self._on_edge(y, dy):
            return False

        return self._color_match(y + dy, dy, x + dx, dx, color)

    # Insert piece at selected field
    def insert(self, row, column, color):
        new = Piece(row, column, color)
        try:
            field = self._board[row][column]
        except IndexError:
            return False
        if field == 0 and (row, column) in self._legal_moves:
            self._board[row][column] = new
            self._flip_board(row, column, color)
            self._last = (row, column)
            # self.all_legal_moves(color)
            if color == WHITE:
                self._white += 1
                self._playing = BLACK
            else:
                self._black += 1
                self._playing = WHITE
            return True
        else:
            return False

    # Flip all encapsulated pieces
    def _flip_board(self, row, column, color):

        self._flip_line(row, -1, column, -1, color)
        self._flip_line(row, -1, column, 0, color)
        self._flip_line(row, -1, column, 1, color)
        self._flip_line(row, 0, column, 1, color)
        self._flip_line(row, 1, column, 1, color)
        self._flip_line(row, 1, column, 0, color)
        self._flip_line(row, 1, column, -1, color)
        self._flip_line(row, 0, column, -1, color)

    # Flip encapsulated pieces in certain direction
    def _flip_line(self, y, dy, x, dx, color):

        if self._on_edge(x, dx) or self._on_edge(y, dy):
            return False
        if self._board[y + dy][x + dx] == 0:
            return False
        if self._board[y + dy][x + dx].color == color:
            return True

        if self._flip_line(y + dy, dy, x + dx, dx, color):
            self._board[y + dy][x + dx].color = color
            if color == WHITE:
                self._white += 1
                self._black -= 1
            else:
                self._white -= 1
                self._black += 1
            return True
        else:
            return False

    def __str__(self):
        string = "\n    1   2   3   4   5   6   7   8   \n"
        for row in range(ROWS):
            string += f"{row+1} |"
            for column in range(COLUMNS):
                data = self._board[row][column]
                if data == 0:
                    string += "   |"
                elif data.color == BLACK:
                    string += " X |"
                else:
                    string += " O |"
            string += "\n"

        return string



