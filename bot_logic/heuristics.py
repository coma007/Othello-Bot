"""
Module containing functions for calculating heuristics.
"""

from game_structures.Game import *


def calculate_heuristics(board):
    """
    Function for calculating the heuristic based on the current board content.

    :param board: Current state of the board.
    :type board: game_structures.Board.Board

    :return: Heuristic value.
    :rtype: float
    """

    color = board.playing

    return heuristics_score(board, color)


def heuristics_score(board, color):
    """
    Helper function for calculating the heuristic.

    :param board: Current state of the board.
    :type board: game_structures.Board.Board
    :param color: Player making the move.
    :type color: tuple[int, int, int]

    :return: Heuristic value.
    :rtype: float
    """

    board_total_score = board_heuristics(board, color)
    pieces_score = pieces_number_heuristics(board, color)
    corners_total_score = corners_heuristics(board, color)

    return board_total_score + pieces_score + corners_total_score


def mobility_heuristics(this_legal, other_legal):
    """
    Helper function for calculating the heuristic value based on one player's mobility relative to the other and the number of adjacent pieces.

    :param this_legal: Number of legal moves for the player making the move.
    :type this_legal: int
    :param other_legal: Number of legal moves for the other player after the move is made.
    :type other_legal: int

    :return: Heuristic value.
    :rtype: float
    """

    if this_legal > other_legal:
        mobility_score = (100.0 * this_legal)/(this_legal + other_legal)
    elif this_legal < other_legal:
        mobility_score = -(100.0 * this_legal)/(this_legal + other_legal)
    else:
        mobility_score = 0

    mobility_score *= 78.922

    return mobility_score


def board_heuristics(board, color):
    """
    Helper function for calculating the heuristic value based on the positions of pieces on the board and the number of adjacent pieces.

    :param board: Current state of the board.
    :type board: game_structures.Board.Board
    :param color: Player making the move.
    :type color: tuple[int, int, int]

    :return: Heuristic value.
    :rtype: float
    """

    row1 = [20, -3, 11,  8,  8, 11, -3, 20]
    row2 = [-3, -7, -4,  1,  1, -4, -7, -3]
    row3 = [11, -4,  2,  2,  2,  2, -4, 11]
    row4 = [+8,  1,  2, -3, -3,  2,  1,  8]
    row5 = [+8,  1,  2, -3, -3,  2,  1,  8]
    row6 = [11, -4,  2,  2,  2,  2, -4, 11]
    row7 = [-3, -7, -4,  1,  1, -4, -7, -3]
    row8 = [20, -3, 11,  8,  8, 11, -3, 20]

    heuristics = [row1, row2, row3, row4, row5, row6, row7, row8]
    board_score = 0

    front_row = [-1, -1, 0, 1, 1, 1, 0, -1]
    front_col = [0, 1, 1, 1, 0, -1, -1, -1]
    this_front = 0
    other_front = 0

    tokens = board.state
    for row in range(ROWS):
        for col in range(COLUMNS):
            token = tokens[row][col]
            if token != 0:
                if token.color == color:
                    board_score += heuristics[row][col]
                else:
                    board_score -= heuristics[row][col]
                for k in range(ROWS):
                    x = row + front_row[k]
                    y = col + front_col[k]
                    if 0 <= x < 8 and 0 <= y < 8 and tokens[x][y] == 0:
                        if token.color == color:
                            this_front += 1
                        else:
                            other_front += 1

    if this_front > other_front:
        front_score = -(100.0 * this_front)/(this_front + other_front)
    elif this_front < other_front:
        front_score = (100.0 * other_front)/(this_front + other_front)
    else:
        front_score = 0

    board_score *= 5
    front_score *= 74.396

    return board_score + front_score


def pieces_number_heuristics(board, color):
    """
    Helper function for calculating the heuristic value based on the number of pieces on the board and the number of adjacent pieces.

    :param board: Current state of the board.
    :type board: game_structures.Board.Board
    :param color: Player making the move.
    :type color: tuple[int, int, int]

    :return: Heuristic value.
    :rtype: float
    """

    black = board.black
    white = board.white

    this_pieces = black
    other_pieces = white
    if color == WHITE:
        this_pieces, other_pieces = other_pieces, this_pieces

    if this_pieces > other_pieces:
        pieces_score = (100.0 * this_pieces)/(this_pieces + other_pieces)
    elif this_pieces < other_pieces:
        pieces_score = -(100.0 * other_pieces)/(this_pieces + other_pieces)
    else:
        pieces_score = 0

    pieces_score *= 500

    return pieces_score


def corners_heuristics(board, color):
    """
    Helper function for calculating the heuristic value based on the positions of pieces on the board relative to the table's corners and the number of adjacent pieces.

    :param board: Current state of the board.
    :type board: game_structures.Board.Board
    :param color: Player making the move.
    :type color: tuple[int, int, int]

    :return: Heuristic value.
    :rtype: float
    """

    tokens = board.state
    corners_score = 0
    near_corner_score = 0

    for i in [0, 7]:
        for j in [0, 7]:
            if tokens[i][j] != 0:
                if tokens[i][j].color == color:
                    corners_score += 1
                else:
                    corners_score -= 1
            else:
                for k in [1, 6]:
                    if tokens[j][k] != 0:
                        if tokens[j][k].color == color:
                            near_corner_score += 1
                        else:
                            near_corner_score -= 1
                    if tokens[k][j] != 0:
                        if tokens[k][j].color == color:
                            near_corner_score += 1
                        else:
                            near_corner_score -= 1
                k = 1
                m = 1
                if i == 7:
                    k = 6
                if j == 7:
                    m = 6
                if tokens[k][m] != 0:
                    if tokens[k][m].color == color:
                        near_corner_score += 1
                    else:
                        near_corner_score -= 1

    corners_score *= 801.724 * 25
    near_corner_score *= -12.5 * 382.026

    return corners_score + near_corner_score
