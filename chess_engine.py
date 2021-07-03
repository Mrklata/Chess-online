# Characterise state of the game
class GameState:
    def __init__(self):
        # 8x8 board
        # lowercase is color b = black; w = white
        # uppercase is a figure
        # '..' = empty field
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["..", "..", "..", "..", "..", "..", "..", ".."],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.white_to_move = True
        self.move_log = []


class Move:
    def __init__(self):
        self.game_state = GameState()
        self.v_l_a = []
        self.v_l_p = []
        self.max_v = range(8)
        self.mv_board = self.game_state.board


    def move(self, player_clicks):
        """
        Define movement
        :param player_clicks: list - list of max two tuples
        :return: str - latest game log
        """
        move_from_row = player_clicks[0][0]
        move_from_col = player_clicks[0][1]
        move_to_row = player_clicks[1][0]
        move_to_col = player_clicks[1][1]

        move_from_piece = self.mv_board[move_from_row][move_from_col]

        self.mv_board[move_to_row][move_to_col] = move_from_piece
        self.mv_board[move_from_row][move_from_col] = ".."

        self.game_state.move_log.append(
            {
                "piece": move_from_piece,
                "from": f"row: {move_from_row}, col: {move_from_col}",
                "to": f"row: {move_to_row}, col: {move_to_col}",
            }
        )

        if (move_from_piece == 'wK') and (move_from_row == move_to_row == 7) and (move_from_col == 4) and (move_to_col == 6):
            self.game_state.white_to_move = not self.game_state.white_to_move
            self.move([(7, 7), (7, 5)])
        
        if (move_from_piece == 'bK') and (move_from_row == move_to_row == 0) and (move_from_col == 4) and (move_to_col == 6):
            self.game_state.white_to_move = not self.game_state.white_to_move
            self.move([(0, 7), (0, 5)])

        
        self.game_state.white_to_move = not self.game_state.white_to_move

        return self.game_state.move_log[-1]

    def position_validation(self, validated_legal_positions):
        self.v_l_p = [
            pose
            for pose in validated_legal_positions
            if self.mv_board[pose[0]][pose[1]] == ".."
        ]

    def attack_validation(self, validated_legal_attacks, picked_piece):
        """

        :param validated_legal_attacks:
        :param picked_piece:
        :return:
        """
        self.v_l_a = [

            attack
            for attack in validated_legal_attacks

            if (
                    (self.mv_board[attack[0]][attack[1]] != "..")
                    and (self.mv_board[attack[0]][attack[1]][0] !=
                         picked_piece[0])
            )
        ]

    def castilng_move(self):

        self.move([(7, 7), (6, 7)])
        pass

    def castling_small(self, picked_piece, colour):
        if colour == 'w':
            data = [colour, 7]
        else:
            data = [colour, 0]
        can_castling = True

        for log in self.game_state.move_log:
            if log['from'] in [f"row: {data[1]}, col: 4", f"row: {data[1]}, col: 7"]:
                can_castling = False
                
        if not (picked_piece[0] == colour and self.mv_board[data[1]][6] == '..' and self.mv_board[data[1]][5] == '..'):
            can_castling = False
        print(can_castling, colour)
        return can_castling

    def clear_out_of_bounds(self, legal_positions):
        """
        clear legal positions of positions 7<lp<0
        :param legal_positions: list - list of lp in which piece can be placed
        :return: list - validated lp
        """

        validated_legal_positions = []

        for pose in legal_positions:
            if (pose[0] in self.max_v) and (pose[1] in self.max_v):
                validated_legal_positions.append(pose)

        return validated_legal_positions

    def until_obstacle(self, move_list, legal_positions, legal_attacks):
        """
        clear list of moves after hitting obstacle and add hitted element to attack list for future validation
        :param move_list: list - list to clear moves
        :param legal_positions: list - list of lp
        :param legal_attacks: list - list of la
        """

        if move_list:

            for pose in self.clear_out_of_bounds(move_list):
                if self.mv_board[pose[0]][pose[1]] == "..":
                    legal_positions.append(pose)

                elif self.mv_board[pose[0]][pose[1]] != "..":
                    legal_attacks.append(pose)
                    break

    def multiple_moves(self, list_moves, legal_positions, legal_attacks, picked_piece):
        """
        call until_obstacle, validate move and attack lists to v_l_p, v_l_a
        :param list_moves:
        :param legal_positions:
        :param legal_attacks:
        :param picked_piece:
        """
        for element in list_moves:
            self.until_obstacle(element, legal_positions, legal_attacks)

        validated_legal_attacks = self.clear_out_of_bounds(legal_attacks)
        self.v_l_p = self.clear_out_of_bounds(legal_positions)

        self.attack_validation(validated_legal_attacks, picked_piece)

    def rules(self, player_clicks):
        """
        specify rules for every piece
        :param player_clicks: list - list of max two tuples
        :return: list - list - lists of validated lp and la
        """
        self.v_l_a = []
        self.v_l_p = []
        legal_positions = []
        legal_attacks = []
        picked_piece = self.mv_board[player_clicks[0][0]][player_clicks[0][1]]
        max_moves = range(1, 9)

        # Moves
        oblique_plus_plus_move = []
        oblique_minus_minus_move = []
        oblique_minus_plus_move = []
        oblique_plus_minus_move = []
        straight_move = []
        back_move = []
        left_move = []
        right_move = []

        # Attacks
        straight_back_attack = []
        left_right_attack = []

        for i in max_moves:
            straight_move.append((player_clicks[0][0] - i, player_clicks[0][1]))
            back_move.append((player_clicks[0][0] + i, player_clicks[0][1]))
            left_move.append((player_clicks[0][0], player_clicks[0][1] + i))
            right_move.append((player_clicks[0][0], player_clicks[0][1] - i))

            oblique_plus_plus_move.append(
                (player_clicks[0][0] + i, player_clicks[0][1] + i)
            )
            oblique_minus_minus_move.append(
                (player_clicks[0][0] - i, player_clicks[0][1] - i)
            )
            oblique_minus_plus_move.append(
                (player_clicks[0][0] - i, player_clicks[0][1] + i)
            )
            oblique_plus_minus_move.append(
                (player_clicks[0][0] + i, player_clicks[0][1] - i)
            )

            straight_back_attack.append((player_clicks[0][0] + i, player_clicks[0][1]))
            straight_back_attack.append((player_clicks[0][0] - i, player_clicks[0][1]))

            left_right_attack.append((player_clicks[0][0], player_clicks[0][1] + i))
            left_right_attack.append((player_clicks[0][0], player_clicks[0][1] - i))

        if picked_piece[1] == "P":
            legal_positions.append(straight_move[0])
            legal_attacks.append(oblique_minus_plus_move[0])
            legal_attacks.append(oblique_minus_minus_move[0])
            if (player_clicks[0][0] == 6) and (self.mv_board[5][player_clicks[0][1]] == '..'):
                legal_positions.append(straight_move[1])

            if picked_piece[0] == "b":
                legal_positions = [(pose[0] + 2, (pose[1])) for pose in legal_positions]
                legal_attacks = [(pose[0] + 2, (pose[1])) for pose in legal_attacks]
                if (player_clicks[0][0] == 1) and (self.mv_board[2][player_clicks[0][1]] == '..'):
                    legal_positions.append(back_move[1])

            validated_legal_positions = self.clear_out_of_bounds(legal_positions)
            validated_legal_attacks = self.clear_out_of_bounds(legal_attacks)

            self.position_validation(validated_legal_positions)

            self.attack_validation(validated_legal_attacks, picked_piece)

        elif picked_piece[1] == "R":
            list_moves = [straight_move, left_move, back_move, right_move]
            self.multiple_moves(
                list_moves, legal_positions, legal_attacks, picked_piece
            )

        elif picked_piece[1] == "N":
            list_moves = [
                (player_clicks[0][0] + 2, player_clicks[0][1] + 1),
                (player_clicks[0][0] + 2, player_clicks[0][1] - 1),
                (player_clicks[0][0] + 1, player_clicks[0][1] + 2),
                (player_clicks[0][0] + 1, player_clicks[0][1] - 2),

                (player_clicks[0][0] - 2, player_clicks[0][1] + 1),
                (player_clicks[0][0] - 2, player_clicks[0][1] - 1),
                (player_clicks[0][0] - 1, player_clicks[0][1] + 2),
                (player_clicks[0][0] - 1, player_clicks[0][1] - 2),
            ]

            validated_legal_positions = self.clear_out_of_bounds(list_moves)
            validated_legal_attacks = validated_legal_positions

            self.position_validation(validated_legal_positions)
            self.attack_validation(validated_legal_attacks, picked_piece)
            print(self.v_l_a)
        elif picked_piece[1] == "B":
            list_moves = [
                oblique_minus_minus_move,
                oblique_plus_plus_move,
                oblique_plus_minus_move,
                oblique_minus_plus_move,
            ]
            self.multiple_moves(
                list_moves, legal_positions, legal_attacks, picked_piece
            )
        elif picked_piece[1] == "Q":
            list_moves = [
                oblique_minus_minus_move,
                oblique_plus_plus_move,
                oblique_plus_minus_move,
                oblique_minus_plus_move,
                left_move,
                right_move,
                back_move,
                straight_move,
            ]
            self.multiple_moves(
                list_moves, legal_positions, legal_attacks, picked_piece
            )
        elif picked_piece[1] == "K":
            list_moves = [
                oblique_minus_minus_move,
                oblique_plus_plus_move,
                oblique_plus_minus_move,
                oblique_minus_plus_move,
                left_move,
                right_move,
                back_move,
                straight_move,
            ]
            for i in list_moves:
                legal_positions.append(i[0])
                legal_attacks.append(i[0])

            validated_legal_positions = self.clear_out_of_bounds(legal_positions)
            validated_legal_attacks = self.clear_out_of_bounds(legal_attacks)

            self.position_validation(validated_legal_positions)
            self.attack_validation(validated_legal_attacks, picked_piece)

            if self.castling_small(picked_piece, picked_piece[0]):
                self.v_l_p.append(((player_clicks[0][0], player_clicks[0][1] + 2)))

        print(f"vla = {self.v_l_a}")
        print(f"vlp = {self.v_l_p}")

        return self.v_l_p, self.v_l_a

    def fields_under_attack(self):
        self.fields_u_a = []
        for row in self.max_v:
            for col in self.max_v:
                player_clicks = (row, col)
                self.fields_u_a.append(self.rules(player_clicks))

        self.fields_u_a = [item for sublist in self.fields_u_a for item in sublist]
