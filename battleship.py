import pedersen
import pickle
import bitproof

class Board:
    LETTERS = {'a': 1, 'b': 2, 'c': 3, 'd': 4,
               'e': 5, 'f': 6, 'g': 7, 'h': 8}
    def __init__(self):
        self.board = [0 for _ in range(64)]

    def get_spot_index(self, spot):
        if int(spot[1]) < 1 or int(spot[1]) > 8 or spot[0] not in self.LETTERS:
            raise ValueError
        return (self.LETTERS[spot[0].lower()] -  1) * 8 + int(spot[1]) - 1

    def get_spot(self, spot):
        return self.board[self.get_spot_index(spot)]
            
    def reset_board(self):
        self.board = [0 for _ in range(64)]

class CommitmentBoard(Board):
    def __init_(self):
        super().__init__(self)
        self.commitment_generator = Pedersen.Pedersen.new_state(64)
        self.commitment_board = [None for _ in range(64)]
        self.public_commitments = [0 for _ in range(64)]
    def update_commitments(self):
            self.commit_board = [self.commitment_generator.commit(x)
                                  for x in self.board]
            self.public_commitments = [x.c for x in  self.commitment_board]
    def send_commitments(self):
        return pickle.dumps(self.public_commitments)
    def send_sum_proof(self):
        return pickle.dumps(Pedersen.add_commitments(*self.commitment_board))
    def send_bit_proof(self):
        return pickle.dumps(
            [bitproof.bit_proof(x, y, self.commitment_generator.state)
             for x, y in zip(self.board, self.commitment_board)]
            )
        
class ShipBoard(Board):
    def input_board(self, t = 8):
        i = 0
        while i < t:
            print(self)
            print(str(i) + (" spot " if i == 1 else " spots ") + "taken")
            a = input()
            try:
                if self.get_spot(a) == 1:
                    print(f"Spot at {a} removed")
                    i -= 1
                else:
                    print(f"Spot at {a} added")
                    i += 1
                self.set_spot(a)
            except ValueError:
                print(f"{a} is not a spot on the board")
                continue
            except IndexError:
                print(f"{a} is not a spot on the board")
                continue
        
    def __repr__(self):
        a = ' '
        for i in range(8):
            a += ' ' + str(i + 1)
        it = iter(self.LETTERS.items())
        for i, s in enumerate(self.board):
            a += '\n' + next(it)[0] + ' ' if (i) % 8 == 0 else ' '
            a += 'X' if s == 1 else '-'
        return a

    def set_spot(self, *spots):
        for spot in spots:
            self.board[self.get_spot_index(spot)] ^= 1


class GuessBoard(Board):
    def __repr__(self):
        a = ' '
        for i in range(8):
            a += ' ' + str(i + 1)
        it = iter(self.LETTERS.items())
        for i, s in enumerate(self.board):
            a += '\n' + next(it)[0] + ' ' if (i) % 8 == 0 else ' '
            a += 'X' if s == 2 else 'x' if s == 1 else '-'
        return a

    def set_spot(self, spot, value):
        self.board[self.get_spot_index(spot)] = value 


                
    
class Game:
    def __init__(self):
        self.turn = True
        self.boards = [ShipBoard(), ShipBoard()]
        self.guesses = [GuessBoard(), GuessBoard()]
        self.playing = False
        self.score =[0, 0]
    def setup(self):
        print("Player 1's board") 
        self.boards[0].input_board()
        print("Player 2's board")
        self.boards[1].input_board()
       
    def play(self):
        guess = 0 if self.turn else 1
        board = 1 if self.turn else 0
        p = 0 if self.turn else 1
        while True:
            print(self.guesses[guess])
            a = input("Input a coordinate to guess: \n")
            try:
                if self.guesses[guess].get_spot(a) == 0:
                    v = self.boards[board].get_spot(a)
                    self.guesses[guess].set_spot(a, 2 if v == 1 else 1)
                    if v ==1:
                        self.score[p] += 1
                        print(f"Spot at {a} is a hit!")
                    else:
                        print(f"Spot at {a} is a miss")
                    break
            except ValueError:
                print(f"{a} is not a spot on the board")
                continue
            except IndexError:
                print(f"{a} is not a spot on the board")
                continue
            
    def game(self):
        while True:
            self.play()
            self.turn ^= True
            if self.score[0] == 8 or self.score[1] == 8:
                print(self.boards[0])
                print(self.boards[1])
                print(self.guesses[0])
                print(self.guesses[1])
                print("Player {} won!".format(1 if self.score[0] = 8 else 2))


