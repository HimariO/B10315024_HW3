from RSA import *

rsa = RSA(key_len=2048)
Y = rsa.encrpy(123456789)
X = rsa.decrpy(Y)

print("encryed: ", Y)
print("decryed: ", X)
