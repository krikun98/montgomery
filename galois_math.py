class Galois:
    def __init__(self, irp=int("100011011", 2)):
        self.irp = irp

    def __mont_init__(self):
        self.k = self.irp.bit_length() - 1
        self.r = 1 << self.k
        self.rt = self.r ^ self.irp
        self.r_sq = self.mult(self.rt, self.rt)

    def __gf2divmod(self, avec, bvec):
        na = avec[0].bit_length()
        nd = bvec[0].bit_length()
        i = na - nd
        q = 0
        test = 1 << (na - 1)
        while i >= 0:
            if (avec[0] & test) != 0:
                avec = [a ^ (d << i) for (a, d) in zip(avec, bvec)]
                q |= (1 << i)
            i -= 1
            test >>= 1
        r = avec
        return q, r

    def __blankinship(self, a, b):
        arow = [a, 1, 0]
        brow = [b, 0, 1]
        while True:
            (_, rrow) = self.__gf2divmod(arow, brow)
            if rrow[0] == 0:
                break
            arow = brow
            brow = rrow
        return tuple(brow)

    def mult(self, a, b):
        k = self.irp.bit_length() - 1
        irp_mult = self.irp - (1 << k)
        p = 0
        while a > 0 and b > 0:
            c = 0
            if b & 1:
                p ^= a
            b >>= 1
            a <<= 1
            if a & 1 << k:
                c = 1
                a -= 1 << k
            if c & 1:
                a ^= irp_mult
        return p

    def add(self, a, b):
        return a ^ b

    def dumb_exp(self, a, e):
        c = 1
        for i in range(e):
            c = self.mult(c, a)
        return c

    def exp(self, a, e):
        c = 1
        r = a
        while e > 0:
            if e & 1:
                c = self.mult(c, r)
            e >>= 1
            if e > 0:
                r = self.mult(r, r)
        return c

    def exp_ltor(self, a, e):
        c = 1
        for i in range(e.bit_length() - 1, -1, -1):
            c = self.mult(c, c)
            if e & 1 << i:
                c = self.mult(c, a)
        return c

    def inv(self, a):
        _, u, _ = self.__blankinship(a, self.irp)
        return u

    def mon_redc(self, a):
        r = 1 << self.irp.bit_length() - 1
        _, irp_tick, r_inv = self.__blankinship(self.irp, r)
        m = (self.mult((a & (r - 1)), irp_tick) & (r - 1))
        t = self.mult((a ^ self.mult(m, self.irp)), r_inv)
        if t > self.irp:
            return t ^ self.irp
        else:
            return t

    def dumb_mon_mult(self, a, b):
        t = self.mult(a, b)
        return self.mon_redc(t)

    def mon_mult(self, a, b):
        c = 0
        for i in range(0, self.irp.bit_length() - 1):
            if (1 << i) & a:
                c = c ^ b
            if 1 & c:
                c = c ^ self.irp
            c >>= 1
        return c

    def montify(self, a):
        return self.mon_mult(a, self.r_sq)

    def mon_square(self, a):
        c = 0
        k = self.irp.bit_length()
        for i in range(k - 1):
            c += (a & 1) << 2 * i
            a >>= 1
        for i in range(k - 1):
            if c & 1:
                c ^= self.irp
            c >>= 1
        return c

    def mon_exp(self, a, e):
        self.__mont_init__()
        c = self.montify(1)
        m = self.montify(a)
        for i in range(self.k):
            if e & (1 << i):
                c = self.mon_mult(c, m)
            m = self.mon_square(m)
        return self.mon_redc(c)

    def mon_mult_and_square(self, m, c):
        t = m
        mul = 0
        sqr = 0
        for i in range(self.irp.bit_length() - 2, -1, -1):
            if t & 1:
                t = t ^ self.irp
            t >>= 1
            if c & (1 << i):
                mul ^= t
            if m & (1 << i):
                sqr ^= t
        return sqr, mul

    def mon_exp_kor(self, a, e):
        self.__mont_init__()
        c = self.montify(1)
        m = self.montify(a)
        for i in range(self.k):
            if e & (1 << i):
                m, c = self.mon_mult_and_square(m, c)
            else:
                m = self.mon_square(m)
        return self.mon_redc(c)
