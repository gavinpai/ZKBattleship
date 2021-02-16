import secrets
import is_prime

def random_prime(bitLength):
    x = secrets.randbits(bitLength-1) * 2 + 1
    while (not is_prime.is_prime(x)):
        x += 2;
    return x;
print(random_prime(512))
    
