"""
Glavni modul.
"""

__author__ = "Milica Sladaković"
__index__ = "SV 18/2020"
__course__ = "Algoritmi i strukture podataka, SIIT, FTN, 2021."
__project__ = "Othello/Reversi Game"


from gameplay import *
from data_structures.HashMap import *
from data_structures.GameTree import *


def select_mode():
    """
    Funkcija za biranje režima u kom se pokreće igra.

    :return: 1 ako je režim konzolni, 2 ako je GUI režim.
    :rtype: int
    """

    mode = -1
    print("\nGAME MODE: ", "\n 1 - Console mode \n 2 - GUI mode")
    while mode not in ["1", "2"]:
        mode = input("\nSelect game mode: ")
    return int(mode)


def init_game():
    """
    Funkcija za inicijalizaciju osnovnih struktura koje će se koristiti tokom igre.

    :return: Strukture i podaci potrebni za nastavak igre.
    :rtype: tuple[Game, HashMap, Tree, int]
    """

    mode = select_mode()
    game = Game(mode)
    hash_map = HashMap()
    game_root = TreeNode(deepcopy(game.board))
    game_tree = Tree(game_root)
    for row, col in game.board.legal_moves:
        tmp_board = deepcopy(game.board)
        tmp_board.insert(row, col, BLACK)
        game_root.add_child(TreeNode(tmp_board))
    return game, hash_map, game_tree, mode


def begin():
    """
    Funkcija za inicijalizaciju igre.
    """

    game, hash_map, game_tree, mode = init_game()
    if mode == 1:
        try:
            pygame.quit()
        except Exception:
            pass
        play_console(game, hash_map, game_tree)
    elif mode == 2:
        WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
        game.window = WINDOW
        main_gui(mode, game, hash_map, WINDOW, game_tree)


if __name__ == '__main__':

    begin()
