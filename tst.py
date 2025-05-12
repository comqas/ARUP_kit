from Crypto.PublicKey.RSA import import_key
from Crypto.Hash import SHAKE256, SHA3_256
from random import randint
from math import log2
from os import urandom
def fail(msg):
	print("fail: "+str(msg))
	quit()

with open("rsra_pub.pem") as f:
	pem = f.read()
RSAp = import_key(pem)
e = RSAp.e
n = RSAp.n
ln = int(log2(n)+0.5)//2

def get_es(e):
	primetab = (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59)
	es = []

	while e>1:
		e = e // primetab[0]
		es.append(primetab[0])
		primetab = primetab[1:]
	return(tuple(es))

es = get_es(e)
print(es)


def blindsig(m,public_key = RSAp):
	n = public_key.n
	e = public_key.e
	es = get_es(e)
	blind = int.from_bytes(urandom(ln//4)) % n
	b1 = pow(blind,e,n)
	b2 = int.from_bytes(urandom(ln//4)) % n
	store = SHAKE256.new()
	store.update(m.to_bytes(ln//4))
	digest = int.from_bytes(store.read(ln//4)) % n
	print("digest:",digest)
	
	bb=b2*blind % n
	################ sending message, getting response
	s1, s2, meta = getsig(digest*b1 % n, bb)
	################
	# check s2
	if s2*bb % n !=1:
		fail("inversion")
	blindi = s2*b2 % n
	# construct e'
	thee = e
	extra=1
	thes = list(es)
	M=meta
	while M>0:
		f = thes.pop()
		if M%2: 
			thee = thee // f
			extra = extra * f
		M = M//2
	# e' = thee, now compute unblinding factor

	u = pow (blindi, extra, n)
	sig = s1*u % n
	# check sig
	if pow(sig, thee, n) == digest:
		print(">>>> checks OK", extra, thee, extra*thee)
	else:
		fail("RSA consistency check fails")
	return sig, meta


with open("rsra.pem") as f:
	pem = f.read()
RSAs = import_key(pem)

def getsig(m, toinv, secret_key = RSAs):
	d = secret_key.d
	es = get_es(secret_key.e)
	meta = getmeta(m)
	thed = d
	thes = list(es)
	M = meta
	while M>0:
		f = thes.pop()
		if M%2: 
			thed = thed * f
		M = M//2
	# sign now
	sig = pow(m,thed, n)
	inverted = pow(toinv, -1, n)
	return sig, inverted, meta
	
m = randint(2^290,2^300) % n

def getmeta(m):
	return 62

print (blindsig(m))



quit()



