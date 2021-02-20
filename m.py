import pickle
import Pedersen
import secrets
import hashlib
#testing adding commitments
"""
a = Pedersen.Pedersen.new_state()
print("Done!")
aa = a.state
b = a.commit(11)
c = a.commit(12)
d = a.commit(23)
l = [b,c]
print(b.c * c.c % a.state.q)
print(d.c)
e = Pedersen.Pedersen_Commit_Output((b.c*c.c)%aa.p, (b.r + c.r)%aa.p)
print(e.c)
print(a.verify(23, e))
f = Pedersen.Pedersen_Commit_Output.add_commitments(a.state,*l)
print(a.verify(23, f))
"""
# Testing object sending
"""
#print(a.state.p)
#b = pickle.dumps(a.state)
#print(b)
#c = pickle.loads(b)
#print(c.p)
"""

# Prove that I know how to open without opening
"""
a = Pedersen.Pedersen.new_state()
b = a.commit(11)
y = secrets.randbelow(a.state.q) # P
s = secrets.randbelow(a.state.q) # P
d = pow(a.state.g,y,a.state.p)*pow(a.state.h,s,a.state.p)%a.state.p # P to V
e = secrets.randbelow(a.state.q) # V to P
u = (y + e * 11) % a.state.q # P to V
v = (s + e * b.r) % a.state.q # P to V
testA = pow(a.state.g,u,a.state.p)*pow(a.state.h,v,a.state.p)%a.state.p
testB = d * pow(b.c,e,a.state.p) % a.state.p
print(testA)
print(testB)
"""
# testing out bit testing (incomplete)
"""
# PROVER
pcg = Pedersen.Pedersen.new_state()
x = 0
c = pcg.commit(x)
ccc = pow(pcg.state.h, c.r, pcg.state.p)
h = pcg.state.h
q = pcg.state.q
g = pcg.state.g
w = secrets.randbelow(q)
y1 = secrets.randbelow(q)
e1 = secrets.randbelow(q)
print("t1")
x0 = pow(h, w, q) # P to V
print("t2")
x1 = pow(h, y1, q) * pow(ccc // g, e1, q) % q # P to V
print("t3")
# VERIFIER
e = secrets.randbelow(q) # V to P
# PROVER
e0 = (e - e1) % q # semds with e1
print("t4")
y0 = (w + c.r * e0) % q #sends with y1
print("t5")
# VERIFIER
print(e, (e0 + e1) % q)
print(x0, (pow(h,y0,q) * pow(ccc,e0,q)))
print(x1, (pow(h,y1,q) * pow(ccc//g,e1,q)))
"""
#Testing adding same commitment
"""
a = Pedersen.Pedersen.new_state()
b = a.commit(5)
c = Pedersen.Pedersen_Commit_Output.add_commitments(a.state, b, b)
print(a.verify(10,c))
"""
#Ring signature test
def hash_int(int):
    return int.from_bytes(hashlib.sha256((int).to_bytes(16, "big")).digest(), "big") 
"""
u = secrets.randbelow(32)+ 1
v = hash_int(u)
v = hash_int(v ^ pow((secrets.randbelow(32) + 1), 2)) % 5
v = hash_int(v ^ pow((secrets.randbelow(32) + 1), 3)) % 7
v = pow(hash_int(u % v),4) % 6
"""
p = [secrets.randbelow(64) + 1 for i in range(2)]
s = [secrets.randbelow(64) + 1 for i in range(2)]
n = [secrets.randbelow(256) + 1 for i in range(2)]
u = secrets.randbelow(32)+ 1
v = hash_int(u)
for i in range(2):
    v = hash_int(v ^ (pow(s[i], p[i]) % n[i]) % n[i])
v = pow(hash_int(u % v),4) % 7
print(a)

