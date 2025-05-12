from Crypto.Hash import SHA256, SHAKE256
from consts import modlen
def H_bar(*argv ):
    r = SHA256.new()
    for arg in argv:
        r.update(arg)
    return r.digest()

def H(*argv):
    r = SHAKE256.new()
    for arg in argv:
        r.update(arg)
    return int.from_bytes(r.read(modlen//8))

def makebytes(x,len):
    if len=='L': return x.to_bytes(modlen//8,'big')
    if len=='M': return x.to_bytes(32,'big')
    if len=='S': return x.to_bytes(1,'big')
    raise ValueError("Incorrect length code: "+str(len))

def Hm(*argv, fmt = None):
    if not fmt: ValueError("fmt=?")
    i = 0
    bytst = bytes()
    for f in fmt:
        if f == '.':
            bytst = bytst + argv[i]
        else:
            bytst = bytst + makebytes(argv[i],f)
        i += 1
    return H(bytst)