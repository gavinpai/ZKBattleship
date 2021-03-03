from board import *
import pickle
import pedersen
import bitproof
import functools
import asyncio
import os
import time

async def poll(x):
    while True:
        await asyncio.sleep(.0001)
        if x() and x() != False:
                return x
        
class Player:
    
    CLEAR = "cls" # Different depending on operating system or interpreter
    
    def __init__(self, t, n):
        self.turn = t
        self.name = n
        self.board = ShipBoard()
        self.guess = GuessBoard()
        self.playing = False
        self.score = 0
        self.commitments = None
        self.other = None
        self.op = None

    async def test_proofs(self, x):
        assert len(x[0]) == 64
        assert pedersen.Pedersen.verify(8, x[1], x[3])
        assert (functools.reduce(lambda z, y: z * y % x[3].p, x[0])
                == x[1].c)
        for c, b in zip(x[0], x[2]):
            assert bitproof.verify(c, x[3], b)
        
            
    async def setup(self, other):
        print(f"Board {self.name}:")
        self.board.input_board(lambda : os.system(CLEAR))
        self.board.update_commitments()
        self.other = other
        self.other.commitments = self.board.commitment_board
        b = other.get_proofs()
        x = pickle.loads(await b)
        await self.test_proofs(x)
        self.commitments = x[0]
        self.op = x[3]
        while True:
            await poll(lambda: self.turn)
            await self.ask()
            self.turn = False
            other.turn = True
            if self.score == 8:
                print("Game over")
                time.sleep(3)
                raise SystemExit
        
    async def get_proofs(self):
        await poll(lambda: self.commitments)
        return self.board.send_initial()

    def get(self, a):
        x = self.board.get_spot(a)
        y = self.board.get_commitment(a)
        return pickle.dumps((x, y))
        

    async def ask(self):
        print(f"Player {self.name}'s turn")
        while True:
            os.system(self.CLEAR)
            print(self.guess)
            a = input("Input a coordinate to guess: \n")
            try:
                if self.guess.get_spot(a) == 0:
                    x = pickle.loads(self.other.get(a))
                    assert pedersen.Pedersen.verify(x[0], x[1], self.op)
                    self.guess.set_spot(a, 2 if x[0] == 1 else 1)
                    os.system(self.CLEAR)
                    print(self.guess)
                    if x[0] == 1:
                        self.score += 1
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
        time.sleep(3)

async def main():
    a = Player(True, 0)
    b = Player(False, 1)
    c = asyncio.create_task(a.setup(b))
    d = asyncio.create_task(b.setup(a))
    await c
    await d

asyncio.run(main())
