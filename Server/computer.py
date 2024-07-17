#from constants import *
import random

class ComputerMove:
    @staticmethod
    def get_random_computer_move(board):
        available_moves = []

        for start_row in range(8):
            for start_col in range(8):
                piece = board[start_row][start_col]

                if piece == 'c':
                    available_moves.extend(ComputerMove.get_moves_for_piece(board, 'c', start_row, start_col))
                elif piece == 'Q':
                    available_moves.extend(ComputerMove.get_moves_for_piece(board, 'Q', start_row, start_col))

        if available_moves:
            capture_moves = [move for move in available_moves if abs(move[1] - move[3]) == 2]
            if capture_moves:
                return random.choice(capture_moves)
            else:
                return random.choice(available_moves)
        else:
            return None

    @staticmethod
    def get_moves_for_piece(board, piece, start_row, start_col):
        moves = []

        if piece == 'c':
            # Normal moves for 'c': moving one step diagonally forward left or right
            ComputerMove.add_move_if_valid(board, moves, piece, start_row, start_col, start_row + 1, start_col - 1)
            ComputerMove.add_move_if_valid(board, moves, piece, start_row, start_col, start_row + 1, start_col + 1)

            # Jump moves for 'c': capturing opponent's piece by jumping over it
            ComputerMove.add_capture_move_if_valid(board, moves, piece, start_row, start_col, start_row + 2, start_col - 2)
            ComputerMove.add_capture_move_if_valid(board, moves, piece, start_row, start_col, start_row + 2, start_col + 2)

        elif piece == 'Q':
            # Moves for 'Q': moving one step diagonally in any direction
            for d_row, d_col in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                ComputerMove.add_move_if_valid(board, moves, piece, start_row, start_col, start_row + d_row, start_col + d_col)

            # Capture moves for 'Q': capturing opponent's piece diagonally
            for d_row, d_col in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
                ComputerMove.add_capture_move_if_valid(board, moves, piece, start_row, start_col, start_row + d_row, start_col + d_col)

        return moves

    @staticmethod
    def add_move_if_valid(board, moves, piece, start_row, start_col, end_row, end_col):
        if 0 <= end_row < 8 and 0 <= end_col < 8 and board[end_row][end_col] == ' ':
            moves.append((piece, start_row, start_col, end_row, end_col))

    @staticmethod
    def add_capture_move_if_valid(board, moves, piece, start_row, start_col, end_row, end_col):
        if 0 <= end_row < 8 and 0 <= end_col < 8:
            captured_row, captured_col = (start_row + end_row) // 2, (start_col + end_col) // 2
            if board[end_row][end_col] == ' ' and board[captured_row][captured_col] == 'p':
                moves.append((piece, start_row, start_col, end_row, end_col))

