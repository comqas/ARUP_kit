from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits
from Crypto.PublicKey.RSA import import_key

from ARUP_Exceptions import *
from ARUP_message import *

from consts import * #t,t_hat,g,eps,modlen
from hash_based import *

class ARUP_client:
    def __init__(self,chlen):
            # initialise round variables
            self.R = None
            self.b1 = self.b2 = self.B = self.W = None
            self.alpha = self.nu = self.phi = None
            self.a_prime = None; self.a = 0
            self.k = 0

            # Winternitz chain
            self.z = [get_random_bytes(32)]
            for j in range(chlen):
                self.z = [H_bar(self.z[0])]+self.z

            # obtain moduli
            with open("RA_pub.pem") as f:
                RAk = import_key(f.read())
            with open("RS_pub.pem") as f:
                RSk = import_key(f.read())
            self.n_hat = RAk.n
            self.n = RSk.n

    def Step1(self,M7):
        if self.k>0:
            a_ast, s1, s2 = M7.extract("SLL")
            if pow(s1,g[eps(self.a,a_ast)],self.n) == (self.B and
                self.W*s2 % self.n == 1): pass # verification
            else:
                raise VerificationError("Step 1")
            coupon = s1*pow(s2*self.b2), t[self.a]//g[eps(self.a,a_ast)] % self.n
            self.a_prime = a_ast
        else:
            coupon = 0
            self.a_prime = 0
        self.phi = get_random_bytes(32)
        if self.k==0: self.nu = get_random_bytes(32)
        self.b1 = getrandbits(modlen) % self.n_hat
        self.b2 = getrandbits(modlen) % self.n_hat
        self.B = H(self.phi)*pow(self.b1, t_hat[self.a], self.n_hat) % self.n
        self.W = self.b2*pow(self.b1, t_hat[self.a], self.n_hat) % self.n
        self.alpha = H_bar(self.B,self.W,self.a,self.a_prime, self.nu, 1 if self.k>0 else 0)
        return Message(coupon,
                              H_bar(self.z[self.k+1],self.nu),
                              self.B, self.W,
                              self.a, self.a_prime,
                              self.alpha,
                       fmt = "LMLLSSM")

    def Step3(self, M2):
        r = M2.extract("L")
        if pow(r, g[1], self.n_hat) == Hm(self.B, self.W, self.a,self.a_prime, self.alpha) % self.n_hat:
            pass # verification
        else:
            raise VerificationError("Step 3")

        self.k += 1
        return Message(self.z[self.k], self.nu, fmt="MM")

    def Step5(self, M4, R):
        self.R = R
        a_ast, s1, s2 = M4.extract("SLL")
        if pow(s1, g[eps(a_ast)]) == self.B:
            pass # verification
        else:
            raise VerificationError("Step 5")
        self.a = a_ast
        cert = s1*pow(s2*self.b2, t_hat[self.a]/g[eps(self.a)]) % self.n_hat

        self.B = H(H_bar(self.z[self.k+1], self.nu))*pow(self.b1,t[self.a],self.n) % self.n
        self.W = self.b2*pow(self.b1,t[self.a]) % self.n

        self.alpha = H_bar(cert,self.a, self.B, self.W, self.alpha, R)

        return Message(cert, self.a, self.B, self.W, self.alpha, self.phi, R, fmt="LSLLMB")

    def Step7(self, M6):
        r = M6.extract("L")
        if pow(r,g[1],self.n) == Hm(self.a, self.B, self.W, self.alpha, self.R) % self.n_hat:
            pass # verification
        else:
            raise VerificationError("Step 7")
        return Message(self.phi, fmt="M")

if __name__ == "__main__":
    mycl = ARUP_client(10)
    print (mycl.Step1(None))
