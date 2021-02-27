import random_prime
import secrets
import dataclasses


class Pedersen:
    """Generates, holds, and verifies Pedersen Commitments"""

    def __init__(self, bit_length = 256):
        """Creates new state for Pedersen Commitment"""
        q = random_prime.schnorr_prime_randbits(bit_length)
        p = q * 4 + 1
        a = secrets.randbelow(q)
        g = Pedersen.generator(p, q)
        h = pow(g, a, p)
        self.state = Pedersen.Public_State(p, q, g, h)

    @dataclasses.dataclass
    class Public_State:
        """Class holding the public variables of the Pedersen commitment"""
        p: int
        q: int
        g: int
        h: int

    @dataclasses.dataclass
    class Commit_Output:
        """Holds the output of a Pedersen Commitment"""
        c: int
        r: int

    def generator(p, q):
        """Returns generator value for Pedersen Commitment that has order q"""
        g = secrets.randbelow(q)
        while pow(g,q,p) != 1:
            g += 2
        if (g > q):
            return generator(p, q)
        return g

    def commit_r(state, x, r):
        """Commits x with a predetermined random number"""
        return Pedersen.Commit_Output(pow(state.g, x, state.p)
                                      * pow(state.h, r, state.p)
                                      % state.p, r)

    def commit(self, x):
        """Commits x using state"""
        return Pedersen.commit_r(self.state, x, secrets.randbelow(self.state.q))

    def add_commitments(state, *commitments):
        """Adds an arbitrary amount of Pedersen Commitments"""
        c, r = 1, 0
        for commitment in commitments:
            c = c * commitment.c % state.p
            r = (r + commitment.r) % state.p
        return Pedersen.Commit_Output(c, r)

    def verify(x, o_state, p_state):
        """Verifies that x equals the commitments value"""
        return Pedersen.commit_r(p_state, x, o_state.r).c == o_state.c
