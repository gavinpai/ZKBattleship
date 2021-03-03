from board import *
import pickle
import pedersen
import bitproof
import functools
import time
import asyncio
import threading 
##class Game:
##
##    def __init__(self):
##        self.turn = True
##        self.boards = [ShipBoard(), ShipBoard()]
##        self.guesses = [GuessBoard(), GuessBoard()]
##        self.playing = False
##        self.score =[0, 0]
##
##    def setup(self):
##        print("Player 1's board")
##        self.boards[0].input_board()
##        print("Player 2's board")
##        self.boards[1].input_board()
##
##    def play(self):
##        guess = 0 if self.turn else 1
##        board = 1 if self.turn else 0
##        p = 0 if self.turn else 1
##        while True:
##            print(self.guesses[guess])
##            a = input("Input a coordinate to guess: \n")
##            try:
##                if self.guesses[guess].get_spot(a) == 0:
##                    v = self.boards[board].get_spot(a)
##                    self.guesses[guess].set_spot(a, 2 if v == 1 else 1)
##                    if v ==1:
##                        self.score[p] += 1
##                        print(f"Spot at {a} is a hit!")
##                    else:
##                        print(f"Spot at {a} is a miss")
##                    break
##            except ValueError:
##                print(f"{a} is not a spot on the board")
##                continue
##            except IndexError:
##                print(f"{a} is not a spot on the board")
##                continue
##
##    def game(self):
##        while True:
##            self.play()
##            self.turn ^= True
##            if self.score[0] == 8 or self.score[1] == 8:
##                print(self.boards[0])
##                print(self.boards[1])
##                print(self.guesses[0])
##                print(self.guesses[1])
##                print("Player {} won!".format(
##                    1 if self.score[0] == 8 else 2))

async def poll(x):
    while True:
        await asyncio.sleep(.0001)
        if x() and x() != False:
                return x
        
class Player:
    def temp(self):
        self.board.set_spot("a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8")
    def __init__(self, t, n):
        self.turn = t
        self.name = n
        self.board = ShipBoard()
        self.guess = GuessBoard()
        self.playing = False
        self.score =[0, 0]
        self.commitments = None
        self.other = None
        self.op = None

    async def test_proofs(self, x):
        assert len(x[0]) == 64
        assert pedersen.Pedersen.verify(8, x[1], x[3])
        print(x[0])
        print(x[3])
        assert (functools.reduce(lambda z, y: z * y % x[3].p, x[0]) == x[1].c)
        
        for c, b in zip(x[0], x[2]):
            assert bitproof.verify(c, x[3], b)
        
            
    async def setup(self, other):
        print(self.name)
        self.temp()
        self.board.update_commitments()
        self.other = other
        self.other.commitments = self.board.commitment_board
        b = other.get_proofs()
        x = pickle.loads(await b)
        await self.test_proofs(x)
        self.commitments = x[0]
        self.op = x[3]
        while True:
            a = poll(lambda: self.turn)
            await a
            z = self.ask()
            await z 
            self.turn = False
            other.turn = True

        
    async def get_proofs(self):
        z = poll(lambda: self.commitments)
        await z
        return self.board.send_initial()

    def get(self, a):
        x = self.board.get_spot(a)
        y = self.board.get_commitment(a)
        return pickle.dumps(x, y)
        

    async def ask(self):
        while True:
            print(self.guess)
            a = input("Input a coordinate to guess: \n")
            try:
                if self.guess.get_spot(a) == 0:
                    x = self.other.get(a)
                    assert pedersen.Pedersen.verify(x[0], x[1])
                    self.guess.set_spot(a, 2 if x[0] == 1 else 1)
                    if x[0] == 1:
                        self.score[n] += 1
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
async def main():
    a = Player(True, 0)
    b = Player(False, 2)
    c = asyncio.create_task(a.setup(b))
    d = asyncio.create_task(b.setup(a))
    await c
    await d

asyncio.run(main())
