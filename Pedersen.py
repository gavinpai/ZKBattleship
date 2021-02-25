import random_prime
import secrets

def generator(p, q):
    """Returns generator value for Pedersen Commitment that has order q"""
    g = secrets.randbelow(q)
    while pow(g,q,p) != 1:
        g += 2
    if (g > q):
        return generator(p, q)
    return g

class Pedersen_Public_State:
    def __init__(self, p, q, g, h):
        """Initializes a structure holding the public variables of the
        Pedersen commitment
        """
        self.p = p
        self.q = q
        self.g = g
        self.h = h

class Pedersen_Commit_Output:
    def __init__(self, c, r):
        """Initializes a structure to hold a commitment and random number"""
        self.c = c
        self.r = r

    def add_commitments(state, *commitments):
        """Adds an arbitrary amount of Pedersen Commitments"""
        c, r = 1, 0
        for commitment in commitments:
            c = c * commitment.c % state.p
            r = (r + commitment.r) % state.p
        return Pedersen_Commit_Output(c, r)

class Pedersen:
    def __init__(self, state, a = None):
        """Initializes a premade Pedersen Commitment"""
        self.state = state
        self.a = a

    def new_state(bit_length = 256):
        """Creates new state for Pedersen Commitment"""
        q = random_prime.schnorr_prime_randbits(bit_length)
        p = q * 4 + 1
        a = secrets.randbelow(q)
        g = generator(p, q)
        h = pow(g, a, p)
        state = Pedersen_Public_State(p, q, g, h)
        return Pedersen(state, a)

    def commit_r(self, x, r):
        """Commits x with a predecided random number"""
        return Pedersen_Commit_Output(pow(self.state.g, x, self.state.p)
                                      * pow(self.state.h, r, self.state.p)
                                      % self.state.p, r)

    def commit(self, x):
        """Commits x using state"""
        return self.commit_r(x, secrets.randbelow(self.state.q))

    def verify(self, x, state):
        """Verifies that x equals the commitments value"""
        return self.commit_r(x, state.r).c == state.c
