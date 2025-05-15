from Crypto.Hash import SHA256, SHAKE256
from consts import modlen


def __int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def H_bar(*argv ):
    r = SHA256.new()
    for arg in argv:
        if isinstance(arg, int):
            r.update(__int_to_bytes(arg))
        elif isinstance(arg, str):
            r.update(arg.encode('utf-8'))
        else:
            r.update(arg)
    return r.digest()

def H(*argv):
    r = SHAKE256.new()
    for arg in argv:
        if isinstance(arg, int):
            r.update(__int_to_bytes(arg))
        elif isinstance(arg, str):
            r.update(arg.encode('utf-8'))
        else:
            r.update(arg)
    return int.from_bytes(r.read(modlen//8))

def makebytes(x,len):
    if len=='L': return x.to_bytes(modlen//8,'big')
    if len=='M': return x.to_bytes(32,'big')
    if len=='S': return x.to_bytes(1,'big')
    raise ValueError("Incorrect length code: "+str(len))
