from game_structures.Game import *

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
    board = node.data.state
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

def gen_hash():

    table = init_table()
    hashes = {}

    return table, hashes
