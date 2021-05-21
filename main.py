from GUI import *

if __name__ == '__main__':

    # Inicijalizacija igre
    game = Game(WINDOW)
    print(game.console())
    print(game._legal_moves)
    start = time()


    # Kreiranje stabla igre



    main_GUI(game)


    while True:

        if game._turn == BLACK:
            row = int(input("Red: "))
            column = int(input("Column: "))
            moved = game.play(row, column)
            if moved:
                elapsed_time = time() - start
                start = time()
                print("Elapsed time black: ", elapsed_time)

        winner = game.winner()
        if winner is not None:
            print("Winner is : ", winner)
            break

        if game._turn == WHITE:
            row, col = ai_play(game.board, table, hash_map)
            moved = game.play(row, col)
            if moved:
                elapsed_time = time() - start
                start = time()
                print("Elapsed time white: ", elapsed_time)

                print(game._legal_moves)

        winner = game.winner()
        if winner is not None:
            print("Winner is : ", winner)
            break

