from dbg import dpr
from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits
from Crypto.PublicKey.RSA import import_key
from math import lcm
from ARUP_Exceptions import *
from ARUP_message import *

from consts import *
from hash_based import *


# obtain moduli
with open("RA.pem") as f:
    RAk = import_key(f.read())
with open("RS_pub.pem") as f:
    RSk = import_key(f.read())
n_hat = RAk.n
n = RSk.n
expm = lcm((RAk.p - 1), (RAk.q - 1))

g_inv = list(g)
for i in range(1, len(g)):
    g_inv[i] = pow(g[i], -1, expm)

a=0
phi = get_random_bytes(32)
b1 = getrandbits(modlen) % n_hat
b2 = getrandbits(modlen) % n_hat
hphi = H(phi) % n_hat
B = hphi * pow(b1, t_hat[a], n_hat) % n_hat
W = b2 * b1  % n_hat    ###### dumb, dumb mistake!!

s1 = pow(B, g_inv[eps(a)],n_hat)
s2 = pow(W,-1,n_hat)

unblinded = s1*pow(s2*b2 % n_hat, t_hat[a]//g[eps(a)], n_hat) % n_hat
direct = pow(hphi, g_inv[eps(a)], n_hat)
decrypted = pow(direct, g[eps(a)], n_hat)
decu = pow(unblinded, g[eps(a)], n_hat)

dpr('hash', hphi, 'unb', unblinded, 'dir', direct, 'decr', decrypted, 'decu', decu)


