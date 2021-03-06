"""
Modul sa klasom Board.
"""

from game_structures.Piece import *


class Board(object):
    """
    Klasa Board modeluje trenutno stanje table.
    """

    def __init__(self, mode, state=None):
        """
        Konstruktor klase Board.

        :param mode: Režim igranja.
        :type mode: int
        :param state: Stanje na tabli.
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
        Privatna metoda koja kreira inicijalno stanje na tabli.
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
        Privatna metoda koja se koristi u GUI režimu kako bi se u prozoru iscrtala sva polja na tabli.

        :param window: Prozor.
        :type window: pygame.Surface
        """

        if self._mode == 2:
            window.fill(GREEN1)
            for row in range(ROWS):
                for col in range(row % 2, ROWS, 2):
                    pygame.draw.rect(window, GREEN2, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw(self, window):
        """
        Metoda koja se koristi u GUI režimu kako bi se u prozoru iscrtale sve figurice.

        :param window: Prozor.
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
        Metoda koja računa sve legalne poteze za trenutno stanje table.

        :param color: Boja igrača za koga se traže legalni potezi.
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
        Privatna metoda koja računa sve legalne poteze za trenutno stanje table u svim smjerovima.

        :param row: Red.
        :type row: int
        :param column: Kolona.
        :type column: int
        :param color: Boja igrača za koga se traže legalni potezi.
        :type color: tuple[int, int, int]

        :return: True ako je moguće odigrati potez na datom polju, u suprotnom False.
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
        Privatna metoda koja računa sve legalne poteze za trenutno stanje table u pojedinačnom smjeru.

        :param y: Horizontalna pozicija.
        :type y: int
        :param dy: Pomak po horizontali.
        :type dy: int
        :param x: Horizontalna pozicija.
        :type x: int
        :param dx: Pomak po horizontali.
        :type dx: int
        :param color: Boja igrača za koga se traže legalni potezi.
        :type color: tuple[int, int, int]

        :return: True ako je moguće odigrati potez u datom smjeru, u suprotnom False.
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
        Privatna metoda koja provjerava da li je protivnik enkapsuliran odigranim potezom.

        :param y: Horizontalna pozicija.
        :type y: int
        :param dy: Pomak po horizontali.
        :type dy: int
        :param x: Horizontalna pozicija.
        :type x: int
        :param dx: Pomak po horizontali.
        :type dx: int
        :param color: Boja igrača za koga se traže legalni potezi.
        :type color: tuple[int, int, int]

        :return: True ako se protivnik enkapsulira, u suprotnom False.
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
        Privatna metoda koja provjerava da li je pozicija blizu ivica table.

        :param a: Pozicija.
        :type a: int
        :param da: Pomak.
        :type da: int

        :return: True ako je pozicija blizu ivice table, u suprotnom False.
        :rtype: bool
        """

        return a + da < 0 or a + da > 7

    def insert(self, row, column, color):
        """
        Metoda kojom se u trenutno stanje ubacuje nova figurica. Ukoliko je ubacivanje figurice uspješno, potez će biti
        odigran, u suprotnom neće.

        :param row: Red.
        :type row: int
        :param column: Kolona.
        :type column: int
        :param color: Boja igrača za koga se traže legalni potezi.
        :type color: tuple[int, int, int]

        :return: True ako je potez odigran, u suprotnom False.
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
        Privatna metoda kojom se enkapsulirane protivničke figurice nakon odigranog poteza prevrću u svim smjerovima.

        :param row: Red.
        :type row: int
        :param column: Kolona.
        :type column: int
        :param color: Boja igrača za koga se traže legalni potezi.
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
        Privatna metoda kojom se enkapsulirane protivničke figurice nakon odigranog poteza prevrću u jednom smjeru.

        :param y: Horizontalna pozicija.
        :type y: int
        :param dy: Pomak po horizontali.
        :type dy: int
        :param x: Horizontalna pozicija.
        :type x: int
        :param dx: Pomak po horizontali.
        :type dx: int
        :param color: Boja igrača za koga se traže legalni potezi.
        :type color: tuple[int, int, int]

        :return: True ako su se protivničke figurice prevrnule, u suprotnom False.
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
