"""
Modul sa osnovnim funkcijama vezanim za igru bot_logic-a.
"""

from bot_logic.heuristics import *
from data_structures.GameTree import *
from math import inf
from copy import deepcopy
from time import time


def bot_play(board, hash_map, current_node):
    """
    Glavna funkcija za odigravanje poteza bot_logic-a, tj. bijelog igrača.

    :param board: Trenutno stanje na tabli..
    :type board: game_structures.Board.Board
    :param hash_map: Heš mapa.
    :type hash_map: data_structures.HashMap.HashMap
    :param current_node: Trenutni čvor stabla.
    :type current_node: data_structures.GameTree.TreeNode

    :return: Red i kolonu polja na kome će se odigrati potez i dubinu na kojoj je izvršena pretraga najboljeg poteza.
    :rtype: tuple[int,int,int]
    """

    elapsed_time = 0
    depth = variable_depth(board, elapsed_time)
    row, col = minimax(board, depth, hash_map, current_node, elapsed_time)[1]

    return row, col, depth


def variable_depth(state, elapsed_time):
    """
    Pomoćna funkcija koja evaluira dubinu u odnosu na trenutno stanje nad kojim se vrši minimax algoritam.

    :param state: Trenutno stanje na tabli.
    :type state: game_structures.Board.Board
    :param elapsed_time: Proteklo vrijeme od početka poteza.
    :type elapsed_time: float

    :return: Dubina.
    :rtype: int
    """

    legal_possibilites = len(state.legal_moves)
    if elapsed_time > 2.5:
        return 1
    if legal_possibilites > 8:
        return 3
    elif legal_possibilites > 5:
        return 4
    else:
        return 5


def minimax(state, depth, hash_map, current_node, elapsed_time, player=WHITE, alpha=-float(inf), beta=float(inf)):
    """
    Minimax algoritam sa alfa-beta rezom.
    bot_logic je bijeli igrač, dakle u ovom slučaju je bijeli igrač Maximizer, a crni Minimizer.

    :param state: Trenutno stanje na tabli.
    :type state: game_structures.Board.Board
    :param depth: Dubina.
    :type depth: int
    :param hash_map: Heš mapa.
    :type hash_map: data_structures.HashMap.HashMap
    :param current_node: Trenutni čvor stabla.
    :type current_node: data_structures.GameTree.TreeNode
    :param elapsed_time: Proteklo vrijeme od početka poteza.
    :type elapsed_time: float
    :param player: Igrač na potezu.
    :type player: tuple[int,int,int]
    :param alpha: Minimalan rezultat koji može da se dobije.
    :type alpha: float
    :param beta: Maksimalan rezultat koji može da se dobije.
    :type beta: float

    :return: Heurističku vrijednost, najbolji potez, broj mogućih poteza.
    :rtype: tuple[int,tuple[int,int],int]
    """

    if depth == 0 or len(state.legal_moves) == 0:
        start = time()
        future_legal_moves = 0
        if len(state.legal_moves) != 0:
            for legal_row, legal_column in state.legal_moves:
                tmp_board = deepcopy(state)
                color = WHITE
                if tmp_board.playing == WHITE:
                    color = BLACK
                tmp_board.insert(legal_row, legal_column, color)
                future_legal_moves = max(future_legal_moves, len(tmp_board.legal_moves))
        try:
            value = hash_map[state.state][0]
        except KeyError:
            value = calculate_heuristics(state)
            value += mobility_heuristics(len(state.legal_moves), future_legal_moves)
            hash_map[state.state] = value, state, future_legal_moves
        elapsed_time += time() - start
        return value, (None, None), future_legal_moves, elapsed_time

    if player == WHITE:
        value = -100000000
        best_move = None
        now_legal_moves = 0
        for legal_row, legal_column in state.legal_moves:
            if elapsed_time > 2.5:
                break
            tmp_board = deepcopy(state)
            tmp_board.insert(legal_row, legal_column, WHITE)
            tmp_legal_moves = len(tmp_board.legal_moves)
            for current_child in current_node.children:
                if tmp_board == current_child.data:
                    new_node = current_child
                    break
            else:
                new_node = TreeNode(deepcopy(tmp_board))
                current_node.add_child(new_node)
            if (legal_row, legal_column) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                best_move = (legal_row, legal_column)
                break
            new_depth = variable_depth(tmp_board, elapsed_time)
            if new_depth <= depth:
                depth = new_depth
            try:
                new_value, new_state, future_legal_moves = hash_map[tmp_board.state]
            except KeyError:
                start = time()
                new_value, last_move, future_legal_moves = minimax(tmp_board, depth - 1, hash_map, new_node, elapsed_time, BLACK, alpha, beta)[0:3]
                hash_map[tmp_board.state] = new_value, last_move, future_legal_moves
                elapsed_time += time() - start
            value = max(value, new_value)
            alpha = max(alpha, value)
            if value == new_value:
                best_move = (legal_row, legal_column)
                now_legal_moves = tmp_legal_moves
            if elapsed_time > 2.5:
                break
            if beta <= alpha:
                break
        if best_move is None:
            best_move = state.legal_moves[0]
        return value, best_move, now_legal_moves, elapsed_time

    else:
        value = 100000000
        best_move = None
        now_legal_moves = 0
        for legal_row, legal_column in state.legal_moves:
            if elapsed_time > 2.5:
                break
            tmp_board = deepcopy(state)
            tmp_board.insert(legal_row, legal_column, BLACK)
            tmp_legal_moves = len(tmp_board.legal_moves)
            for current_child in current_node.children:
                if tmp_board == current_child.data:
                    new_node = current_child
                    break
            else:
                new_node = TreeNode(deepcopy(tmp_board))
                current_node.add_child(new_node)
            new_depth = variable_depth(tmp_board, elapsed_time)
            if new_depth < depth - 1:
                depth = new_depth
            try:
                new_value, new_state, future_legal_moves = hash_map[tmp_board.state]
            except KeyError:
                start = time()
                new_value, last_move, future_legal_moves = minimax(tmp_board, depth - 1, hash_map, new_node, elapsed_time, WHITE, alpha, beta)[0:3]
                hash_map[tmp_board.state] = new_value, last_move, future_legal_moves
                elapsed_time += time() - start
            value = min(value, new_value)
            beta = min(beta, value)
            if value == new_value:
                best_move = (legal_row, legal_column)
                now_legal_moves = tmp_legal_moves
            if elapsed_time > 2.5:
                break
            if beta <= alpha:
                break
        if best_move is None:
            best_move = state.legal_moves[0]
        return value, best_move, now_legal_moves, elapsed_time
