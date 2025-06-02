from dbg import dpr
from Crypto.PublicKey.RSA import import_key
from ARUP_Exceptions import *
from ARUP_message import *
from consts import *
from hash_based import *
from sqlite3 import *
from math import lcm
from RUP import Upd

class RS:
    def __init__(self, cache_lim=100):
        with open("RA_pub.pem") as f:
            RAk = import_key(f.read())
        with open("RS.pem") as f:
            RSk = import_key(f.read())
        self.n = RSk.n
        self._d = RSk.d
        self.n_hat = RAk.n
        self._expm = lcm((RSk.p - 1), (RSk.q - 1))

        self.conn = connect(":memory:")
        self.c = self.conn.cursor()
        self.c.execute('CREATE TABLE KVS ("tag" BLOB NOT NULL, "value" BLOB)')
        self.c.execute('CREATE TABLE "blocked" ("tag" BLOB, PRIMARY KEY("tag"))')
        self.conn.commit()

        self.lastinout5 = {}
        self.cache_size5 = 0
        self.lastinout7 = {}
        self.cache_size7 = 0
        self.cache_lim = cache_lim


        self.g_inv = list(g)
        for _i in range(1,len(g)):
            self.g_inv[_i] = pow(g[_i],-1,self._expm)


    def Step6(self, M5):
        if M5 in self.lastinout5: return self.lastinout5[M5]
        cert, a, B, W,  alpha, R = M5.extract("LSLLMB")
        h = pow(cert,g[eps(a)],self.n_hat)     #h = H(phi)
        self.c.execute("SELECT ? in blocked as outcome",(H_bar(h),))
        if self.c.fetchone():
            VerificationError("Step 6")
        self.conn.execute("INSERT INTO KVS (tag,value) VALUES (?,?)",
                       (H_bar(h),
                                    Message(a, B, W, alpha, R, fmt="SLLMB").dump()
                                   )
                       )
        self.conn.commit()
        M6 = Message(pow(H(a, B, W, alpha, R) % self.n, self.g_inv[1], self.n), fmt="L")
        self.lastinout5[M5] = M6
        self.cache_size5 += 1
        if self.cache_size5 > self.cache_lim:
            del self.lastinout5[list(self.lastinout5)[0]]
            self.cache_size5 -= 1
        return M6

    def Step8(self, M7):
        if M7 in self.lastinout7: return self.lastinout7[M7]
        (phi,) = M7.extract("M")
        h = H(phi) % self.n_hat
        queue_tag = H_bar(h)
        self.c.execute("SELECT value FROM KVS WHERE tag = ?", (queue_tag,))
        verified = False
        dbdata = self.c.fetchall()
        for (qel,) in dbdata:
            qelm = Message(qel, packed=True)
            a, B, W, alpha, R = qelm.extract("SLLMB")
            if alpha == H_bar(B, W, a, phi, R):
                verified = True
                break
        if verified: pass  # verification
        else:
            self.c.execute("select tag FROM KVS")
            raise VerificationError("Step8")
        # execute
        self.c.execute("INSERT INTO blocked (tag) VALUES (?)", (queue_tag,))
        self.c.execute("DELETE FROM KVS WHERE tag = ?",(queue_tag,))
        self.conn.commit()
        a_star = Upd(a,R)
        s1 = pow(B, self.g_inv[eps(a, a_star)], self.n)
        s2 = pow(W,-1,self.n)
        M8 = Message(a_star,s1,s2,fmt="SLL")
        self.lastinout7[M7]=M8
        self.cache_size7 += 1
        if self.cache_size7 > self.cache_lim:
            del self.lastinout7[list(self.lastinout7)[0]]
            self.cache_size7 -= 1
        return M8
if __name__ == "__main__":
    obj = RA()
    print(obj._expm)
