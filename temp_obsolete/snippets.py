
#code snippets for later
a = Pedersen.new_state()
b = a.commit(11)
y = secrets.randbelow(a.state.q) # P
s = secrets.randbelow(a.state.q) # P
d = pow(a.state.g,y,a.state.p)*pow(a.state.h,s,a.state.p)%a.state.p # P to V
e = secrets.randbelow(a.state.q) # V to P
u = y + e * b.x # P to V
v = (s + e * b.r) % a.state.q # P to V
testA = pow(a.state.g,u,a.state.p)*pow(a.state.h,v,a.state.p)%a.state.p
testB = d * pow(b.c,e,a.state.p) % a.state.p
print(testA)
print(testB)
