from client import client
from RA import RA
from RS import RS
from random import randint

ra = RA()           # launch Registration Authority
rs = RS()           # launch Reputation Server

cl = client()
print("{:X}".format(cl.n))
