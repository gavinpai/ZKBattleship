import Pedersen
import pickle
class Board:
    def __init__(self):
        self.commitment_generator = Pedersen.Pedersen.new_state(64)
        self.board = [[0 for i in range(8)] for j in range(8)]
        self.commit_board = [[None for i in range(8)] for j in range(8)]
        self.public_commitments = [[None for i in range(8)] for j in range(8)]
    def toggle_spot(self, *args):
        for arg in args:
            self.board[arg[0]][arg[1]] ^= 1;
    def reset_board(self):
        self.board = [[0 for i in range(8)] for j in range(8)]
        self.update_commitments()
    def update_commitments(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                self.commit_board[i][j] = self.commitment_generator.commit(self.board[i][j])
                self.public_commitments[i][j] = self.commit_board[i][j].public_commitment();
    def send_commitments(self):
        return pickle.dumps(self.public_commitments)
    def verify_commitments(self):
        for i in self.commit_board:
            for j in i:
                print(self.commitment_generator.verify(1, j))
b = Board()
b.toggle_spot((1,2))
b.update_commitments()
print(b.send_commitments())
b.verify_commitments()

