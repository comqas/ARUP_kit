import inspect
def dpr(*args):
    indent = '   '
    ln ="*** function:"+str(inspect.stack()[1].function)+'\n'
    for arg in args:
        if isinstance(arg, int):
            if arg<10**20:
                ln +=indent+str(arg)+'\n'
            else:
                ln +=indent+str(arg)[:10]+'...\n'
        if isinstance(arg, str):
                ln += arg + ': '
        if isinstance(arg, bytes) or isinstance(arg,bytearray):
                ln += arg.hex()[:20]+'...\n'
    print(ln)

