from Crypto.PublicKey.RSA import import_key
from ARUP_Exceptions import *
from ARUP_message import *
from ARUP_message import *
from consts import *
from hash_based import *
from sqlite3 import *
from math import lcm
from hash_based import *
from consts import *
from RUP import Adj,Upd
from json import dumps, loads


class RA:
    def __init__(self):
        with open("RA.pem") as f:
            RAk = import_key(f.read())
        with open("RS.pem") as f:
            RSk = import_key(f.read())
        self.n = RSk.n
        self._d = RAk.d
        self.n_hat = RAk.n
        self._expm = lcm((RAk.p - 1), (RAk.q - 1))
        self.conn = connect(":memory:")
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE KVS ("tag" BLOB NOT NULL, "value" BLOB)')
        self.c.execute('CREATE TABLE "blocked" ("tag" BLOB, PRIMARY KEY("tag"))')
        self.lastinout1 = {}
        self.lastinout3 = {}
        self.g_inv = list(g)
        for _i in range(1,len(g)):
            self.g_inv[_i] = pow(g[_i],-1,self._expm)


    def Step2(self, M1):
        if M1 in self.lastinout1: return self.lastinout[M1]
        coupon, z, B, W, a, a_prim, alpha = M1.extract("LLMLLSSM")
        self.c.execute("SELECT ? in blocked as outcome",(z,))
        (outcome,) = self.c.fetchone
        if outcome: VerificationError("Step 2.i")
        if coupon == 0:
            pass  # verification
        elif pow(coupon, g[eps(a, a_prim)], self.n) % self.n == H(z) % self.n:
            pass  # verification
        else:
            raise VerificationError("Step 2.ii")
        self.c.execute("INSERT INTO KVS (tag,value) VALUES (?,?)",
                       (z,
                        Message(B, W, a, a_prim, alpha).to_bytes()
                        )
                       )
        out = Message(pow(H(B, W, a, a_prim, alpha), self.g_inv[1], self.n_hat), fmt="L")
        self.lastinout1[M1] = out
        return out

    def Step4(self, M3):
        if M3 in self.lastinout3: return self.lastinout3[M3]
        z, nu = M3.extract("MM")
        Hbarz = H_bar(z)
        self.c.execute("SELECT value FROM KVS WHERE tag = ?", (Hbarz,))
        asigma = self.c.fetchone()
        if asigma:
            pass  # verification
        else:
            raise VerificationError("Step3.i")
        a, sigma = loads(asigma[0])
        queue_key = H_bar(z, nu)
        self.c.execute("SELECT value FROM KVS WHERE tag = ?", (queue_key,))
        verified = False
        for qel in self.c.fetchall():
            qelm = Message(qel, bytx=True)
            B, W, a_star, a_prime, alpha = qelm.extract("LLSSM")
            if a == a_star and alpha == H_bar(B, W, a_star, a_prime, nu, sigma is None):
                verified = True
                break
        if verified: pass  # verification
        else:
            raise VerificationError("Step3.ii")
        # execute
        self.c.execute("DELETE FROM KVS WHERE tag = ?",(Hbarz,))
        self.c.execute("DELETE FROM KVS WHERE taf = ?",(queue_key,))
        self.c.execute("INSERT INTO blocked (tag) VALUES (?)", z)
        self.conn.commit()
        a, sigma_prime = Adj(a_prime, sigma)
        self.c.execute("INSERT into KVS (tag, value) VALUES (?,?)",(z,dumps(a,sigma_prime)))
        self.conn.commit()
        s1 = pow(B,self.g_inv[eps(a)], self.n_hat)
        s2 = pow(W,-1,self.n_hat)
        M4 = Message(a,s1,s2,fmt="SLL")
        self.lastinout[M3]=M4
        return M4
if __name__ == "__main__":
    obj = RA()
    print(obj._expm)
