# Characterise state of the game
class GameState:
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

    def pond_rules(self, player_clicks):
        picked_piece = self.board[player_clicks[0][0]][player_clicks[0][1]]
        destination_piece = self.board[player_clicks[1][0]][player_clicks[1][1]]
        # White pond rules
        # Basic move
        if picked_piece[0] == 'w':
            legal_positions = [[
                player_clicks[0],
                (player_clicks[0][0] - 1, player_clicks[0][1])
            ]]
            # First move
            if player_clicks[0][0] == 6:
                legal_positions.append([
                    player_clicks[0],
                    (player_clicks[0][0] - 2, player_clicks[0][1])
                ])
            # Attack
            if destination_piece != '..':
                legal_positions = [
                    [player_clicks[0],
                     (player_clicks[0][0] - 1, player_clicks[0][1] + 1)
                     ],
                    [player_clicks[0],
                     (player_clicks[0][0] - 1, player_clicks[0][1] - 1)
                     ]
                ]
        # Black pond rules
        # Basic move
        elif picked_piece[0] == 'b':
            legal_positions = [[
                player_clicks[0],
                (player_clicks[0][0] + 1, player_clicks[0][1])
            ]]
            # First move
            if player_clicks[0][0] == 1:
                legal_positions.append([
                    player_clicks[0],
                    (player_clicks[0][0] + 2, player_clicks[0][1])
                ])

            if destination_piece != '..':
                legal_positions = [
                    [player_clicks[0],
                     (player_clicks[0][0] + 1, player_clicks[0][1] + 1)
                     ],
                    [player_clicks[0],
                     (player_clicks[0][0] + 1, player_clicks[0][1] - 1)
                     ]
                ]
        else:
            legal_positions = []

        if player_clicks in legal_positions:
            return True

        else:
            return False
