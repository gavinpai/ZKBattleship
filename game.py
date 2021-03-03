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
                print("Player {} won!".format(
                    1 if self.score[0] == 8 else 2))
class Player():
    def __init__(self):
        self.turn = True
        self.board = ShipBoard()
        self.guess = GuessBoard()
        self.playing = False
        self.score =[0, 0]
        self.boards.input_board()
        self.commitments = None
        
    def setup(self, other):
        self.boards.input_board()
        self.other = other
        x = other.get_proofs()
        self.commitments = x[0]
        
    def check(self, x):
        
    def ask(self):
        while True:
            print(self.guess)
            a = input("Input a coordinate to guess: \n")
            try:
                if self.guess.get_spot(a) == 0:
                    while True 
                        v = other.get(a)
                        except ValueError:
                            continue
                        if self.check(v):
                            break
                    self.guess.set_spot(a, 2 if v == 1 else 1)
                    if v == 1:
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
        if not self.turn:
            a = other.get_input()
        else:
            self.ask()
        
