class Decimal:
    def __init__(self, n):
        self.n = n
        self.k = n.bit_length()
        self.r = 1 << self.k
        self.r_sq = self.r * self.r % self.n
        _, n_inv, _ = self.xgcd(self.n, self.r)
        self.n_tick = -n_inv if n_inv < 0 else self.r - n_inv

    def xgcd(self, a, b):
        # return (g, x, y) such that a*x + b*y = g = gcd(a, b)
        x0, x1, y0, y1 = 0, 1, 1, 0
        while a != 0:
            (q, a), b = divmod(b, a), a
            y0, y1 = y1, y0 - q * y1
            x0, x1 = x1, x0 - q * x1
        return b, x0, y0

    def bit_mask(self, t):
        # essentially a modulo with a factor of two
        p = 1 << self.k
        return t & (p - 1)

    def mon_redc(self, t):
        # montgomery reduction (process to get numbers back from montgomery form)
        m = self.bit_mask((self.bit_mask(t) * self.n_tick))
        t = (t + m * self.n) >> self.k
        if t >= self.n:
            return t - self.n
        else:
            return t

    def mon_mult(self, a_mont, b_mont):
        # montgomery modular multiplication (a*b) mod n
        t = a_mont * b_mont
        u = (t + self.bit_mask(t * self.n_tick) * self.n) >> self.k
        if u > self.n:
            return u - self.n
        else:
            return u

    def montify(self, a):
        return self.mon_mult(a, self.r_sq)

    def mon_exp(self, a, e, n):
        a_mont = self.montify(a)
        x = self.montify(1)
        while e > 0:
            if e & 1:
                x = self.mon_mult(x, a_mont)
            a_mont = self.mon_mult(a_mont, a_mont)
            e = e >> 1
        return self.mon_redc(x)
