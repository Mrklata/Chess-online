# Characterise state of the game
class GameState():
    def __init__(self):
        # 8x8 board
        # lowercase is color b = black; w = white
        # uppercase is a figure
        # '..' = empty field
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['..', '..', '..', '..', '..', '..', '..', '..'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.white_to_move = True
        self.move_log = []

    def move(self, player_clicks):
        move_from_row = player_clicks[0][0]
        move_from_col = player_clicks[0][1]
        move_to_row = player_clicks[1][0]
        move_to_col = player_clicks[1][1]

        move_from_piece = self.board[move_from_row][move_from_col]

        self.board[move_to_row][move_to_col] = move_from_piece
        self.board[move_from_row][move_from_col] = '..'

        self.move_log.append({'piece': move_from_piece, 'from': f'row: {move_from_row}, col: {move_from_col}',
                              'to': f'row: {move_to_row}, col: {move_to_col}'})

        if self.white_to_move:
            self.white_to_move = False

        else:
            self.white_to_move = True

        print(self.move_log[-1])
