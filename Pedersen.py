import random_prime
import secrets
import hashlib
import pickle
import dataclasses

class Bit_Proof:
    def __init__(self, message, commitment, state):
        if message == 0:
            e1 = secrets.randbelow(state.p)
            y1 = secrets.randbelow(state.p)
            r = secrets.randbelow(state.p)
            x0 = pow(state.h, r, state.p)
            x1 = (pow(state.h, y1, state.p)
                       * pow(commitment.c * pow(state.g, -1, state.p),
                             -e1, state.p) % state.p)
            e = Bit_Proof.hash_int((x0, x1)) % state.p
            e0 = (e - e1) % state.p
            y0 = (r + commitment.r * e0) % (state.p - 1)
        if message == 1:
            e0 = secrets.randbelow(state.p)
            y0 = secrets.randbelow(state.p)
            r = secrets.randbelow(state.p)
            x1 = pow(state.h, r, state.p)
            x0 = (pow(state.h, y0, state.p)
                       * pow(commitment.c, -e0, state.p) % state.p)
            e = Bit_Proof.hash_int((x0, x1)) % state.p
            e1 = (e - e0) % state.p
            y1 = (r + commitment.r * e1) % (state.p - 1)
        self.state = Bit_Proof.Output(e, e0, e1, x0, x1, y0, y1)

    @dataclasses.dataclass
    class Output:
        e: int
        e0: int
        e1: int
        x0: int
        x1: int
        y0: int
        y1: int
    def hash_int(x):
        """Pickles, hashes, and returns input as an integer"""
        return int.from_bytes(hashlib.blake2b(
            pickle.dumps(x)).digest(),"big")

    def verify(c, p_state, bp_state):
        c_a = (bp_state.e
               == Bit_Proof.hash_int((bp_state.x0, bp_state.x1)) % p_state.p)
        c_b = (bp_state.x1 * pow(c * pow(p_state.g, -1, p_state.p),
                             bp_state.e1, p_state.p) % p_state.p
               == pow(p_state.h, bp_state.y1, p_state.p))
        c_c = (bp_state.x0 * pow(c, bp_state.e0, p_state.p) % p_state.p
               == pow(p_state.h, bp_state.y0, p_state.p))
        c_d = ((bp_state.e1 + bp_state.e0) % p_state.p
               == bp_state.e)
        return c_a and c_b and c_c and c_d

class Pedersen:
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

a = Pedersen(64)
b = a.commit(0)
c = Bit_Proof(0, b, a.state)
print(Bit_Proof.verify(b.c, a.state, c.state))
print(Pedersen.verify(0, b, a.state))
