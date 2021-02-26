import Pedersen
import pickle
class Board:
    def __init__(self):
        self.commitment_generator = Pedersen.Pedersen.new_state(64)
        self.board = [0 for _ in range(64)]
        self.commit_board = [None for _ in range(64)]
        self.public_commitments = [0 for _ in range(64)]
    def toggle_spot(self, *args):
        for arg in args:
            self.board[arg[0] * 8 + arg[1]] ^= 1;
    def reset_board(self):
        self.board = [[0 for i in range(8)] for j in range(8)]
        self.update_commitments()
    def update_commitments(self):
            self.commit_board = [self.commitment_generator.commit(x)
                                  for x in self.board]
            self.public_commitments = [x.c for x in  self.commit_board]
    def send_commitments(self):
        return pickle.dumps(self.public_commitments)
    def verify_commitments(self):
        for m, c in zip(self.board, self.commit_board):
            print(self.commitment_generator.verify(m, c))
b = Board()
b.toggle_spot((1,2))
b.update_commitments()
print(b.send_commitments())
print(b.public_commitments)
b.verify_commitments()

