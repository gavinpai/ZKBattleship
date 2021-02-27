import pickle
import Pedersen
import secrets
import hashlib
import random_prime

#testing adding commitments
def test_add_commitments():
    a = Pedersen.Pedersen.new_state()
    aa = a.state
    b = a.commit(11)
    c = a.commit(12)
    d = a.commit(23)
    l = [b,c]
    e = Pedersen.Pedersen_Commit_Output((b.c * c.c) % aa.p, (b.r + c.r) % aa.p)
    assert(a.verify(23, e))
    f = Pedersen.Pedersen_Commit_Output.add_commitments(a.state, *l)
    assert(a.verify(23, f))

#test sending and loading
def test_send_object():
    a = Pedersen.Pedersen.new_state()
    b = pickle.dumps(a.state)
    c = pickle.loads(b)
    assert(c.p == a.state.p)

#Testing adding same commitment
def test_add_commitment_2():
    a = Pedersen.Pedersen.new_state()
    b = a.commit(5)
    c = Pedersen.Pedersen_Commit_Output.add_commitments(a.state, b, b)
    assert(a.verify(10,c))



def test():
    test_add_commitments()
    test_send_object()
    test_add_commitment_2()



# Cheating prover (e is known)

message = 1
a = Pedersen.Pedersen.new_state(64)
b = a.commit(message)
Q = a.state.q
H = a.state.h
G = a.state.g
P = a.state.p
R = b.r
C = b.c
if message == 0:
    e1 = secrets.randbelow(P)
    y1 = secrets.randbelow(P)
    r = secrets.randbelow(P)
    x0 = pow(H,r, P)
    x1 = pow(H, y1, P) * pow(C*pow(G,-1,P), -e1, P) % P
    e = int.from_bytes(hashlib.blake2b(pickle.dumps((x0, x1))).digest(),
                       "big") % P
    e0 = (e - e1) % P
    y0 = (r + R * e0) % (P - 1)
if message == 1:
    e0 = secrets.randbelow(P)
    y0 = secrets.randbelow(P)
    r = secrets.randbelow(P)
    x1 = pow(H,r, P)
    x0 = pow(H, y0, P) * pow(C, -e0, P) % P
    e = int.from_bytes(hashlib.blake2b(pickle.dumps((x0, x1))).digest(),
                       "big") % P
    e1 = (e - e0) % P
    y1 = (r + R * e1) % (P - 1)
print(e == int.from_bytes(hashlib.blake2b(pickle.dumps((x0, x1))).digest(),
                       "big") % P)
print(x1 * pow(C*pow(G,-1,P), e1, P) % P== pow(H, y1, P))
print(x0 * pow(C, e0, P) % P == pow(H, y0, P))
print((e1 + e0) % P == e)
#send e, e0, e1, x0, x1, y0, y1

