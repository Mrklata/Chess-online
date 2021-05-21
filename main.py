import pygame as pg
import chess_engine


# initiate classes
# move = chess_engine.Move()
mv = chess_engine.Move()
# General game variables
WIDTH = 512
HEIGHT = 512
DIMENSIONS = 8
SQ_SIZE = int(HEIGHT / DIMENSIONS)
MAX_FPS = 15
IMAGES = {}


# Load images
def load_images():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(f'img/{piece}.png'), (SQ_SIZE, SQ_SIZE))


# Main driver
def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color('white'))
    load_images()
    running = True
    sq_selected = ()
    player_clicks = []
    col = None
    row = None
    current_piece = None
    legal_positions = None
    legal_attacks = None

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

            elif e.type == pg.MOUSEBUTTONDOWN:
                location = pg.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                current_piece = mv.game_state.board[row][col]

                if sq_selected == (row, col):
                    sq_selected = ()
                    player_clicks = []

                elif len(player_clicks) == 0 and current_piece == '..':
                    sq_selected = ()

                else:
                    if (len(player_clicks) == 0 and mv.game_state.white_to_move and current_piece[0] == 'w') or\
                            (len(player_clicks) == 0 and not mv.game_state.white_to_move and current_piece[0] == 'b'):
                        sq_selected = (row, col)
                        pg.draw.rect(screen, (0, 0, 255), (SQ_SIZE * col, SQ_SIZE * row, SQ_SIZE, SQ_SIZE))
                        print(f'1sq = {sq_selected}')
                        player_clicks.append(sq_selected)
                        legal_positions = mv.pond_rules(player_clicks)[0]
                        legal_attacks = mv.pond_rules(player_clicks)[1]

                    elif len(player_clicks) == 1:
                        first_picked_piece = mv.game_state.board[player_clicks[0][0]][player_clicks[0][1]]
                        sq_selected = (row, col)
                        print(f'2sq = {sq_selected}')
                        player_clicks.append(sq_selected)
                        print(f'player clicks: {player_clicks}')
                        if first_picked_piece[1] == 'P':
                            for i in mv.game_state.board:
                                print(i)

                            legal_positions = mv.pond_rules(player_clicks)[0]
                            legal_attacks = mv.pond_rules(player_clicks)[1]
                            print(player_clicks[1])
                            print(legal_attacks)
                            print(player_clicks[1] in legal_attacks)
                            if player_clicks[1] in legal_attacks or player_clicks[1] in legal_positions:
                                mv.move(player_clicks)
                                player_clicks = []
                                sq_selected = ()
                            else:
                                player_clicks = []
                                sq_selected = ()
        draw_game_state(screen, col, row, current_piece, player_clicks, legal_positions, legal_attacks)
        clock.tick(MAX_FPS)
        pg.display.flip()


# Drawing game state
def draw_game_state(screen, col, row, current_piece, player_clicks, legal_positions, legal_attacks):
    draw_board(screen)
    if col is not None and current_piece != '..' and len(player_clicks) == 1:
        pg.draw.rect(screen, (0, 200, 0), (SQ_SIZE * col, SQ_SIZE * row, SQ_SIZE, SQ_SIZE))
        for i in legal_positions:
            pg.draw.rect(screen, (0, 255, 0), (SQ_SIZE * i[1], SQ_SIZE * i[0], SQ_SIZE, SQ_SIZE))
        for i in legal_attacks:
            pg.draw.rect(screen, (255, 100, 100), (SQ_SIZE * i[1], SQ_SIZE * i[0], SQ_SIZE, SQ_SIZE))

    draw_pieces(screen, mv.game_state.board)


# Drawing board
def draw_board(screen):
    colors = [pg.Color('light gray'), pg.Color('dark gray')]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[(r+c) % 2]
            pg.draw.rect(screen, color, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


# Drawing pieces
def draw_pieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "..":
                screen.blit(IMAGES[piece], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()
