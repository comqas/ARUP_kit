from Crypto.Hash import SHA256, SHA512
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
    count = modlen//512
    r = [0,1,2,3,4,5,6,7][:count]
    for k in range(count):
        r[k] = SHA512.new()
    for arg in argv:
        for k in range(count):
            kk = bytes([k])
            if isinstance(arg, int):
                r[k].update(__int_to_bytes(arg)+kk)
            elif isinstance(arg, str):
                r[k].update(arg.encode('utf-8')+kk)
            else:
                r[k].update(arg+kk)
    return int.from_bytes(b''.join([x.digest() for x in r]))

def makebytes(x,len):
    if len=='L': return x.to_bytes(modlen//8,'big')
    if len=='M': return x.to_bytes(32,'big')
    if len=='S': return x.to_bytes(1,'big')
    raise ValueError("Incorrect length code: "+str(len))
