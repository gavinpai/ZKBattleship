import random_prime
import secrets

class Pedersen_Public_State:
    def __init__(self, p, q, g, h):
        self.p = p
        self.q = q
        self.g = g
        self.h = h
class Pedersen_Commit_Output:
    def __init__(self, c, r):
        self.c = c
        self.r = r
    def public_commitment(self):
        return self.c
    def add_commitments(state, *commitments):
        c, r = 1, 0
        for commitment in commitments:
            c = c * commitment.c % state.p
            r = (r + commitment.r) % state.p
        return Pedersen_Commit_Output(c, r)
class Pedersen:
    def __init__(self, state, a = None):
        self.state = state
        self.a = a
    def new_state(bit_length = 64):
        q = random_prime.schnorr_prime_randbits(bit_length)
        p = q * 4 + 1
        a = secrets.randbelow(q)
        g = 3
        h = pow(g, a, p)
        state = Pedersen_Public_State(p, q, g, h)
        return Pedersen(state, a)
    def commit_r(self, x, r):
        return Pedersen_Commit_Output(pow(self.state.g, x, self.state.p) * pow(self.state.h, r, self.state.p) % self.state.p, r)
    def commit(self, x):
        return self.commit_r(x, secrets.randbelow(self.state.q))
    def verify(self, x, state):
        return self.commit_r(x, state.r).public_commitment() == state.c


    











    
    
