from Crypto.Util import number
from Crypto.PublicKey.RSA import construct
from math import lcm
from random import randint
from os import urandom
import re
def fail(msg):
	print("fail: "+str(msg))
	quit()

ln = input("key length [2048]:")
if not ln:
	ln = 1024
elif not ln.isdigit():
	fail("illegal number")
else:
	ln = int(ln)/2

es = (3,5,7,11,13,17,19,23,29)

print("Generating RSA key pair, length:",2*ln)
fname = input("file name for the key:")
if not re.match(r'^[A-Za-z0-9_]+$', fname):
	fail("Illegal filename, use alphanumerics")
primes =[]
while len(primes)<2:
	passed = False
	while not passed:
		p = number.getPrime(ln)
		passed = True
		for f in es:
			if p%f == 1:
				passed = False
				break
	primes.append(p)
n = lcm(primes[0],primes[1])
z = (primes[0]-1)*(primes[1]-1)

e = 3
d = pow(e, -1, z)

RSA = construct((n,e,d,primes[0],primes[1]), consistency_check = True)
sk = RSA.export_key()
pk = RSA.public_key().export_key()
with open(fname+".pem","w") as file:
	file.write(sk.decode('ascii'))

with open(fname+"_pub.pem","w") as file:
	file.write(pk.decode('ascii'))
	
print("Files",fname+".pem and",fname+"_pub.pem saved")

quit(0)
