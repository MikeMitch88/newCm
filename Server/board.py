ansi_black = "\u001b[30m"
ansi_red = "\u001b[30m"
ansi_green = "\u001b[30m"
ansi_yellow = "\u001b[30m"
ansi_blue = "\u001b[30m"
ansi_magenta = "\u001b[30m"
ansi_cyan = "\u001b[30m"
ansi_white = "\u001b[30m"
ansi_reset = "\u001b[30m"

class Board:
    def __init__(self):
        self.board=[
            [' ', 'c', ' ', 'c', ' ', 'c', ' ', 'c'],
            ['c', ' ', 'c', ' ', 'c', ' ', 'c', ' '],
            [' ', 'c', ' ', 'c', ' ', 'c', ' ', 'c'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' '],
            [' ', 'p', ' ', 'p', ' ', 'p', ' ', 'p'],
            ['p', ' ', 'p', ' ', 'p', ' ', 'p', ' ']
        ]

    def print_board(self):       
        print()
        print(" ", end=" ")
        for col in range(0,8):
            print(ansi_magenta + f" {col} " + ansi_reset, end=" ")
        print()
        print(" +---+---+---+---+---+---+---+---+")
        for row in range(0,8):
            print(f"{ansi_magenta}{row}{ansi_reset}", end="|")
            for col in range(8):
                piece = self.board[row][col]
                if piece == 'p':
                    piece = ansi_yellow + piece + ansi_reset
                elif piece == 'c':
                    piece = ansi_green + piece + ansi_reset
                print(f" {piece} |", end="")
            print(ansi_magenta + f"{row} {ansi_reset} ")
            print(" +---+---+---+---+---+---+---+---+")
        for col in range(0,8):
            print(f" {ansi_magenta}  {col}{ansi_reset}",end="")
        print()#space after board ptinted out
        print()
              #upadate the pieces that are left 
        #calculate the pieces left, both computer and player
        player_pieces = sum(row.count('p') + row.count('K') for row in self.board)
        computer_pieces = sum(row.count('c') + row.count('Q') for row in self.board)
        print(f"{ansi_green}Player Pieces Left:{ansi_reset}{ansi_yellow} {player_pieces}{ansi_reset}")
        print(f"{ansi_green}Computer Pieces Left: {ansi_reset}{ansi_magenta} {computer_pieces}{ansi_reset}")
        

        
            
# if __name__=="__main__":
#     game=Board()
#     game.board[0][1]='k'
#     game.print_board()