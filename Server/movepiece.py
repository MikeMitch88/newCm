class MovePiece:
    def move_piece(board, piece, start_row, start_col, end_row, end_col):
        
        if abs(start_row - end_row) == 1:
            # Clear the previous position of the piece
            board[start_row][start_col] = ' '

            # Check if the piece reaches the opponent's back row to become a king
            if piece == "c" and end_row == 7:
                board[end_row][end_col] = "CK"  # Crown as COMPKING
            elif piece == "p" and end_row == 0:
                board[end_row][end_col] = "PK"  # Crown as PLAYERking
            else:
                board[end_row][end_col] = piece  # Place the piece at the new position

        # if a capture move (jumping over an opponent's piece)
        if abs(start_row - end_row) == 2:
            board[start_row][start_col] = ' '  # Clear the previous position of the piece

            # Capturing move upwards
            if start_row - end_row == 2:
                # Capturing move to the right
                if start_col - end_col == -2:
                    # Clear the captured piece
                    board[start_row - 1][start_col + 1] = ' '

                    # Promote to queen or king if reached the back row
                    if piece == "c" and end_row == 7:
                        board[end_row][end_col] = "CK"
                    elif piece == "p" and end_row == 0:
                        board[end_row][end_col] = "PK"
                    else:
                        board[end_row][end_col] = piece

                # Capturing move to the left
                elif start_col - end_col == 2:
                    # Clear the captured piece
                    board[start_row - 1][start_col - 1] = ' '

                    # Promote to queen or king if reached the back row
                    if piece == "c" and end_row == 7:
                        board[end_row][end_col] = "CK"
                    elif piece == "p" and end_row == 0:
                        board[end_row][end_col] = "PK"
                    else:
                        board[end_row][end_col] = piece

            # Capturing move downwards
            elif start_row - end_row == -2:
                # Capturing move to the left
                if start_col - end_col == -2:
                    # Clear the captured piece
                    board[start_row + 1][start_col + 1] = ' '

                    # Promote to queen or king if reached the back row
                    if piece == "c" and end_row == 7:
                        board[end_row][end_col] = "CK"
                    elif piece == "p" and end_row == 0:
                        board[end_row][end_col] = "PK"
                    else:
                        board[end_row][end_col] = piece

                # Capturing move to the right
                else:
                    # Clear the captured piece
                    board[start_row + 1][start_col - 1] = ' '

                    # Promote to queen or king if reached the back row
                    if piece == "c" and end_row == 7:
                        board[end_row][end_col] = "CK"
                    elif piece == "p" and end_row == 0:
                        board[end_row][end_col] = "PK"
                    else:
                        board[end_row][end_col] = piece
