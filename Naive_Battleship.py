class Board:
    def __init__(self):
        self.board = [0 for _ in range(64)]
    def toggle_spot(self, *args):
        for arg in args:
            self.board[arg[0] * 8 + arg[1]] ^= 1;
    def reset_board(self):
        self.board = [[0 for i in range(8)] for j in range(8)]



