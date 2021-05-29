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

        move_from_piece = self.game_state.board[move_from_row][move_from_col]

        self.game_state.board[move_to_row][move_to_col] = move_from_piece
        self.game_state.board[move_from_row][move_from_col] = ".."

        self.game_state.move_log.append(
            {
                "piece": move_from_piece,
                "from": f"row: {move_from_row}, col: {move_from_col}",
                "to": f"row: {move_to_row}, col: {move_to_col}",
            }
        )

        self.game_state.white_to_move = not self.game_state.white_to_move

        return self.game_state.move_log[-1]

    # def rules(self, player_clicks):
    #     """
    #     def
    #     :param player_clicks:
    #     :return:
    #     """
    #     picked_piece = self.game_state.board[player_clicks[0][0]][player_clicks[0][1]]
    #     # White pond rules
    #     # Basic move
    #     if picked_piece[0] == "w":
    #         legal_positions = [(player_clicks[0][0] - 1, player_clicks[0][1])]
    #
    #         legal_attacks = [
    #             (player_clicks[0][0] - 1, player_clicks[0][1] + 1),
    #             (player_clicks[0][0] - 1, player_clicks[0][1] - 1),
    #         ]
    #
    #         # First move
    #         if player_clicks[0][0] == 6:
    #             legal_positions.append((player_clicks[0][0] - 2, player_clicks[0][1]))
    #
    #     # Black pond rules
    #     # Basic move
    #     elif picked_piece[0] == "b":
    #         legal_positions = [(player_clicks[0][0] + 1, player_clicks[0][1])]
    #
    #         legal_attacks = [
    #             (player_clicks[0][0] + 1, player_clicks[0][1] + 1),
    #             (player_clicks[0][0] + 1, player_clicks[0][1] - 1),
    #         ]
    #         # First move
    #         if player_clicks[0][0] == 1:
    #             legal_positions.append((player_clicks[0][0] + 2, player_clicks[0][1]))
    #
    #     else:
    #         legal_positions = []
    #         legal_attacks = []
    #
    #     # Validation
    #     validated_lp = []
    #     validated_la = []
    #
    #     for pose in legal_positions:
    #         if self.game_state.board[pose[0]][pose[1]] == "..":
    #             validated_lp.append(pose)
    #
    #     for pose in legal_attacks:
    #         if (
    #             self.game_state.board[pose[0]][pose[1]] != ".."
    #             and self.game_state.board[pose[0]][pose[1]][0] != picked_piece[0]
    #         ):
    #             validated_la.append(pose)
    #
    #     return validated_lp, validated_la

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
        clear list of moves after hitting obstacle
        :param move_list: list - list to clear moves
        :param legal_positions: list - list of lp
        :param legal_attacks: list - list of la
        """

        if move_list:

            for pose in self.clear_out_of_bounds(move_list):
                if self.game_state.board[pose[0]][pose[1]] == "..":
                    legal_positions.append(pose)

                elif self.game_state.board[pose[0]][pose[1]] != "..":
                    legal_attacks.append(pose)
                    break

    def multiple_moves(self, list_moves, legal_positions, legal_attacks, picked_piece):
        for element in list_moves:
            self.until_obstacle(element, legal_positions, legal_attacks)
        # else:
        #     for element in list_moves:
        #         legal_positions.append(element[0])
        #         legal_attacks.append(element[0])
        # legal_positions = [item for sublist in legal_positions for item in sublist]

        validated_legal_positions = self.clear_out_of_bounds(legal_positions)
        validated_legal_attacks = self.clear_out_of_bounds(legal_attacks)

        for pose in validated_legal_positions:
            if self.game_state.board[pose[0]][pose[1]] == "..":
                self.v_l_p.append(pose)
            elif self.game_state.board[pose[0]][pose[1]][0] != picked_piece[0]:
                validated_legal_attacks.append(pose)
                break

        self.v_l_a = [
            attack
            for attack in validated_legal_attacks
            if (
                self.game_state.board[attack[0]][attack[1]] != ".."
                and self.game_state.board[attack[0]][attack[1]][0] != picked_piece[0]
            )
        ]

    def pond_rules(self, player_clicks):
        """
        specify rules for every piece
        :param player_clicks: list - list of max two tuples
        :return: list - list - lists of validated lp and la
        """
        self.v_l_a = []
        self.v_l_p = []
        legal_positions = []
        legal_attacks = []
        picked_piece = self.game_state.board[player_clicks[0][0]][player_clicks[0][1]]
        max_moves = range(1, 9)

        # Moves
        straight_move = []
        for i in max_moves:
            straight_move.append((player_clicks[0][0] - i, player_clicks[0][1]))

        back_move = []
        for i in max_moves:
            back_move.append((player_clicks[0][0] + i, player_clicks[0][1]))

        left_move = []
        right_move = []
        for i in max_moves:
            left_move.append((player_clicks[0][0], player_clicks[0][1] + i))
            right_move.append((player_clicks[0][0], player_clicks[0][1] - i))

        oblique_plus_plus_move = []
        oblique_minus_minus_move = []
        oblique_minus_plus_move = []
        oblique_plus_minus_move = []

        for i in max_moves:
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

        # Attacks
        straight_back_attack = []
        for i in max_moves:
            straight_back_attack.append((player_clicks[0][0] + i, player_clicks[0][1]))
            straight_back_attack.append((player_clicks[0][0] - i, player_clicks[0][1]))

        left_right_attack = []
        for i in max_moves:
            left_right_attack.append((player_clicks[0][0], player_clicks[0][1] + i))
            left_right_attack.append((player_clicks[0][0], player_clicks[0][1] - i))

        oblique_attack = []
        for i in max_moves:
            oblique_attack.append((player_clicks[0][0] + i, player_clicks[0][1] + i))
            oblique_attack.append((player_clicks[0][0] - i, player_clicks[0][1] - i))
            oblique_attack.append((player_clicks[0][0] - i, player_clicks[0][1] + i))
            oblique_attack.append((player_clicks[0][0] + i, player_clicks[0][1] - i))

        if picked_piece[1] == "P":
            legal_positions.append(straight_move[0])
            legal_attacks.append(oblique_attack[1])
            legal_attacks.append(oblique_attack[2])
            if player_clicks[0][0] == 6:
                legal_positions.append(straight_move[1])
            print(legal_positions)

            if picked_piece[0] == "b":
                legal_positions = [(pose[0] + 2, (pose[1])) for pose in legal_positions]
                legal_attacks = [(pose[0] + 2, (pose[1])) for pose in legal_attacks]
                if player_clicks[0][0] == 1:
                    legal_positions.append(
                        (player_clicks[0][0] + 2, player_clicks[0][1])
                    )

            print(legal_positions)

            validated_legal_positions = self.clear_out_of_bounds(legal_positions)
            validated_legal_attacks = self.clear_out_of_bounds(legal_attacks)

            self.v_l_p = [
                pose
                for pose in validated_legal_positions
                if self.game_state.board[pose[0]][pose[1]] == ".."
            ]

            self.v_l_a = [
                attack
                for attack in validated_legal_attacks
                if (
                    self.game_state.board[attack[0]][attack[1]] != ".."
                    and self.game_state.board[attack[0]][attack[1]][0]
                    != picked_piece[0]
                )
            ]
        elif picked_piece[1] == "R":
            list_moves = [straight_move, left_move, back_move, right_move]
            self.multiple_moves(
                list_moves, legal_positions, legal_attacks, picked_piece
            )

        elif picked_piece[1] == "N":
            pass
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

            for pose in validated_legal_positions:
                if self.game_state.board[pose[0]][pose[1]] == "..":
                    self.v_l_p.append(pose)
                elif self.game_state.board[pose[0]][pose[1]][0] != picked_piece[0]:
                    validated_legal_attacks.append(pose)

            self.v_l_a = [
                attack
                for attack in validated_legal_attacks
                if (
                        self.game_state.board[attack[0]][attack[1]] != ".."
                        and self.game_state.board[attack[0]][attack[1]][0] != picked_piece[0]
                )
            ]

        # legal_positions = [item for sublist in legal_positions for item in sublist]
        # legal_attacks = [item for sublist in legal_attacks for item in sublist]

        print(f"vla = {self.v_l_a}")
        print(f"vlp = {self.v_l_p}")

        return self.v_l_p, self.v_l_a
