modlen = 2048
g = [None, 3, 5, 7, 11, 13, 17, 19, 23, 29]
def eps(*argv):
    if len(argv)==1: return argv[0]+1 # eps(a)
    else:
        return {
            (0,0):1,
            (0,1):2,
            (1,0):1,
            (1,1):3,
            (1,2):4,
            (2,0):1,
            (2,1):5,
            (2,2):6,
            (2,3):7,
            (3,0):1,
            (3,2):8,
            (3,3):9
        }[tuple(argv)]


t = [(1,2),(1,3,4),(1,5,6,7),(1,8,9)]
for __k in range(4):
    __a = 1
    for __b in t[__k]:
        __a = __a * g[__b]
    t[__k] = __a

t_hat = [(0,),(1,0,2),(2,1,3),(3,2)]
for __k in range(4):
    __a = 1
    for __b in t_hat[__k]:
        __a = __a * g[eps(__b)]
    t_hat[__k] = __a