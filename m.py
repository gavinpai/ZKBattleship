#import pickle
import Pedersen

#testing code
a = Pedersen.Pedersen.new_state()
aa = a.state
b = a.commit(11)
c = a.commit(12)
d = a.commit(23)
l = [[b,c],[d]]
print(b.c * c.c % a.state.q)
print(d.c)
e = Pedersen.Pedersen_Commit_Output((b.c*c.c)%aa.p, (b.r + c.r)%aa.p)
print(e.c)
print(a.verify(23, e))
f = Pedersen.Pedersen_Commit_Output.add_commitments(a.state,*l)
print(a.verify(23, f))
#print(a.state.p)
#b = pickle.dumps(a.state)
#print(b)
#c = pickle.loads(b)
#print(c.p)
