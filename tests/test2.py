from client import client
from RA import RA
from RS import RS
from random import randint

ra = RA()           # launch Registration Authority
rs = RS()           # launch Reputation Server

def swarm(*args):
    procs = []
    cls = []
    for arg in args:
        cl = client()
        ra.onboard(cl.z[0])  # onboard the client on RA
        M = cl.Step1(None)
        cls.append(cl)
        procs.append((2,M))
    tot = len (cls)
    clock = 0

    while(True):
        active = randint(0,tot-1)
        step, Message = procs[active]
        cl = cls[active]
        print("active process:", active, "step:", step)
        if step == 1:
            M = cl.Step1(Message)
        elif step == 2:
            M = ra.Step2(Message)
        elif step == 3:
            M = cl.Step3(Message)
        elif step == 4:
            M = ra.Step4(Message)
        elif step == 5:
            cl.report("clock {}, client {} report".format(clock,active))
            M = cl.Step5(Message)
        elif step == 6:
            M = rs.Step6(Message)
        elif step == 7:
            M = cl.Step7(Message)
        elif step == 8:
            M = rs.Step8(Message)
        step = step + 1 if step < 8 else 1
        procs[active] = (step, M)
        clock += 1
        if clock % 250 == 0 and input("ticks "+str(clock)+". stop?").startswith('y'): break

swarm(client(),client(),client())
print ("RA Cache usage:", len(ra.lastinout1.keys())+len(ra.lastinout3.keys()))
print ("RS Cache usage:", len(rs.lastinout5.keys())+len(rs.lastinout7.keys()))
