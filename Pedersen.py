import random_prime
import secrets

class Pedersen_Public_State:
    def __init__(self, p, q, g, h):
        self.p = p
        self.q = q
        self.g = g
        self.h = h
class Pedersen_Commit_Output:
    def __init__(self, x, c, r):
        self.c = c
        self.r = r
        self.x = x
    def public_commitment(self):
        return(self.c)
    
class Pedersen:
    def __init__(self, state, a = None):
        self.state = state
        self.a = a
    @classmethod
    def new_state(cls, bit_length = 128):
        q = random_prime.safe_prime(bit_length)
        p = q * 2 + 1
        a = secrets.randbelow(q - 1) + 1
        g = secrets.randbelow(q - 1) + 1
        h = pow(g, a, q)
        state = Pedersen_Public_State(p, q, g, h)
        return Pedersen(state, a)
    def commit_r(self, x, r):
        return(Pedersen_Commit_Output(x, pow(self.state.g, x, self.state.p) * pow(self.state.h, r, self.state.p) % self.state.p, r))
    def commit(self, x):
        return(self.commit_r(x, secrets.randbelow(self.state.q)))
    def verify(self, state):
        return(self.commit_r(state.x, state.r).public_commitment() == state.c)
        

