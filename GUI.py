from AI import *
from time import time

pygame.init()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 200
pygame.display.set_caption("Othello")
font = pygame.font.Font('freesansbold.ttf', 15)

hash_map = {}
table = init_table()


def nortifications(black=2, white=2, last_played="", time=0.00):
    pygame.draw.rect(WINDOW, WHITE, pygame.Rect(0, 700, 700, 30))
    text = font.render(f'      '
                       f'Black: {black}          '
                       f'White: {white}               '
                       f'Elapsed time for the last {last_played} move: {time: .2f} s     ',
                       True, BLACK, WHITE)
    textbox = text.get_rect()
    textbox.center = (700 // 2, 715)

    return text, textbox


def mouse_action(position):

    x, y = position
    row = y // SQUARE_SIZE
    column = x // SQUARE_SIZE

    return row, column


def main_GUI(game):

    clock = pygame.time.Clock()
    start = time()
    run = True
    text, textbox = nortifications()
    game.update()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game._turn == BLACK:
                    position = pygame.mouse.get_pos()
                    row, column = mouse_action(position)
                    moved = game.play(row, column)
                    if moved:
                        elapsed_time = time() - start
                        start = time()
                        text, textbox = nortifications(game.black, game.white, "black", elapsed_time)

        game.update()
        WINDOW.blit(text, textbox)
        winner = game.winner()
        if winner is not None:
            WINDOW.blit(font.render(f"      "
                                    f"Black: {game.black}          "
                                    f"White: {game.white}                          "
                                    f"Game over !      "
                                    f"{winner} won !                  ", True, BLACK, WHITE), textbox)
        pygame.display.update()

        if game._turn == WHITE:
            row, col = ai_play(game.board, table, hash_map)
            moved = game.play(row, col)
            if moved:
                elapsed_time = time() - start
                start = time()
                text, textbox = nortifications(game.black, game.white, "white", elapsed_time)

        game.update()
        WINDOW.blit(text, textbox)
        winner = game.winner()
        if winner is not None:
            WINDOW.blit(font.render(f"      "
                                    f"Black: {game.black}          "
                                    f"White: {game.white}                          "
                                    f"Game over !      "
                                    f"{winner} won !                  ", True, BLACK, WHITE), textbox)
        pygame.display.update()

    pygame.quit()

