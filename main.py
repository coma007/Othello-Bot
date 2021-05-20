from GUI import *

if __name__ == '__main__':

    # Inicijalizacija igre
    game = Game(WINDOW)

    # Kreiranje stabla igre



    # main_GUI(game)

    while True:

        if game._turn == BLACK:
            row = input(print("Insert row"))
            column = input(print("Insert column"))

            game.play(int(row), int(column))

        else:
            row, col = igraj_jadnik(game.board, table, hashes)
            game.play(row, col)

