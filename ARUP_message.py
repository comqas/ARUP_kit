class Message:
    lengths = {'S': 1, 'M': 32, 'L': 256}

    def __init__(self, *argv, fmt=None, packed = False):
        if packed:
            self.content = argv[0].hex()
            return
        if not fmt:
            self.content = argv[0]
            return
        k = 0
        msg = []
        for arg in argv:
            if fmt[k] == 'B':
                msg.append(arg.hex())
                break
            size = Message.lengths[fmt[k]]
            if fmt[k] != 'M':
                msg.append(format(arg,"0"+str(2*size)+"x"))
            else:
                msg.append(arg.hex())
            k += 1
        self.content = ''.join(msg)

    def __str__(self):
        return self.content

    def dump(self):
        return bytes.fromhex(self.content)

    def extract(self,fmt):
        cursor = 0
        parts = []
        lenx = len(self.content)
        for f in fmt:
            if f == 'B':
                parts.append(bytes.fromhex(self.content[cursor:]))
                return tuple(parts)

            size = 2*Message.lengths[f]
            if cursor+size > lenx:
                raise ValueError("Message shorter than required by format")
            hexstring = self.content[cursor:cursor+size]
            if f!='M':
                component = int(hexstring,16)
            else:
                component = bytes.fromhex(hexstring)
            parts.append(component)
            cursor += size
        return tuple(parts)

    def to_bytes(self):
        return bytes.fromhex(self.content)

    def __str__(self):
        return self.content

if __name__ == "__main__":
    x = Message("SSM", 3,5,2**253)
    print(x.content)
    a,b,c = x.extract("SSM")
    print("a={:x} b={:x} c={:064x}".format(a,b,c))