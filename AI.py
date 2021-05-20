from data_structures.GameTree import Tree, TreeNode
from copy import deepcopy
from game_structures.Board import *
from heuristics import *
from game_structures.Game import *
# from GUI import *


def generate_game_tree(node, depth, color=WHITE):

    board = node.data

    if color == BLACK:
        color = WHITE
    else:
        color = BLACK

    if len(board.legal_moves) == 0 or depth == 1:
        return

    # print(board.legal_moves, "\n")

    for legal_move in board.legal_moves:
        row, column = legal_move
        tmp_board = deepcopy(board)
        tmp_board.insert(row, column, color)


        if color == BLACK:
            new_color = WHITE
        else:
            new_color = BLACK

        tmp_board.all_legal_moves(new_color)
        new_legal = len(tmp_board.legal_moves)
        old_legal = tmp_board.old_legal_moves
        # print(old_legal, new_legal)
        # print(tmp_board.legal_moves)
        child = TreeNode(tmp_board)
        # print(child)

        # print(heuristics_score(tmp_board, color, old_legal, new_legal))
        node.add_child(child)

    for child in node.children:
        generate_game_tree(child, depth-1, color)

    # print("odradio stablo")
    return node

# game = Game(WINDOW)

# print(tree_root)
# for children in tree_root.children:
#     print("PARENT")
#     print(children)
#     print("CHILDREN")
#     for child in children.children:
#         print(child)
#     print ("--------")
# tree.breadth(print)
# print(iter)





def value_to_node(node):

    global VALUE
    if VALUE == heuristics(node):
        print(node)


# tree.breadth(value_to_node)

import random

def init_table():

    table = []

    for i in range(8):
        column = []
        for j in range(8):
            numbers = []
            for k in range(2):
                numbers.append(random.randint(0, 255))
            column.append(numbers)
        table.append(column)

    return table


# table = init_table()

def hash_formula(node, table):
    board = node.data.board
    h = 0
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            field = table[i][j]
            if piece != 0:
                if piece.color == WHITE:
                    v = 0
                else:
                    v = 1
                p = field[v]
                h ^= p

    return h


def minimax(node, depth, maximizing_player, table, hashes):

    if depth == 0 or node.is_leaf():
        h = heuristics(node)
        f = hash_formula(node, table)
        hashes[f] = (h, node)
        return h

    if maximizing_player:
        value = -100000000
        for child in node.children:
            value = max(value, minimax(child, depth-1, False, table, hashes))
            h = value
            f = hash_formula(node, table)
            hashes[f] = (h, node)
        return value

    else:
        value = 100000000
        for child in node.children:
            value = min(value, minimax(child, depth-1, True, table, hashes))
            h = value
            f = hash_formula(node, table)
            hashes[str(f)] = (h, node)
        return value

# hashes = {}

#
#
# VALUE = minimax(tree_root, 3, False)
# print(VALUE)
# print(hashes)


def iter_hashes(hashes, value):
    for pos in hashes:
        # print(pos)
        # print(hashes[pos][0])
        if hashes[pos][0] == value:

            new_position = hashes[pos][1]
            row, col = new_position.data.last
            return row, col

def igraj_jadnik(board, table, hashes):

    tree_root = TreeNode(board)
    tree_root = generate_game_tree(tree_root, 4)

    tree = Tree(tree_root)

    value = minimax(tree_root, 2, True, table, hashes)
    print("odradio minimax")
    return iter_hashes(hashes, value)

def gen_hash():

    table = init_table()
    hashes = {}

    return table, hashes
