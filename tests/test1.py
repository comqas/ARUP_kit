from client import client
from RA import RA
from RS import RS

ra = RA()           # launch Registration Authority
rs = RS()           # launch Reputation Server
cl = client()       # launch a client

ra.onboard(cl.z[0])         # onboard the client on RA

# ARUP protocol trace

M1 = cl.Step1(None)
print('M1',M1)
M2 = ra.Step2(M1)
print('M2',M2)
M3 = cl.Step3(M2)
print('M3',M3)
M4 = ra.Step4(M3)
print('M4',M4)
M5 = cl.Step5(M4, "some report")
print('M5',M5)
M6 = rs.Step6(M5)
print('M6',M6)
M7 = cl.Step7(M6)
print('M7',M7)
M8 = rs.Step8(M7)
print('M8',M8)
