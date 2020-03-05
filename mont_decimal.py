class Decimal:


def xgcd(a, b):
    # return (g, x, y) such that a*x + b*y = g = gcd(a, b)
    x0, x1, y0, y1 = 0, 1, 1, 0
    while a != 0:
        (q, a), b = divmod(b, a), a
        y0, y1 = y1, y0 - q * y1
        x0, x1 = x1, x0 - q * x1
    return b, x0, y0


def bit_mask(t, k):
    # essentially a modulo with a factor of two
    p = 1 << k
    return t & (p - 1)


def mon_redc(t, n, n_tick, k):
    # montgomery reduction (process to get numbers back from montgomery form)
    m = bit_mask((bit_mask(t, k) * n_tick), k)
    t = (t + m * n) >> k
    if t >= n:
        return t - n
    else:
        return t


def mon_mult(a_mont, b_mont, n, n_tick, k):
    # montgomery modular multiplication (a*b) mod n
    t = a_mont * b_mont
    u = (t + bit_mask(t * n_tick, k) * n) >> k
    if u > n:
        return u - n
    else:
        return u


def mon_exp(a, e, n):
    k = n.bit_length()
    r = 1 << k
    _, n_inv, _ = xgcd(n, r)
    n_tick = -n_inv if n_inv < 0 else r - n_inv
    r_sq_mont = r * r % n
    a_mont = mon_mult(a, r_sq_mont, n, n_tick, k)
    x = mon_mult(1, r_sq_mont, n, n_tick, k)
    while e > 0:
        if e & 1:
            x = mon_mult(x, a_mont, n, n_tick, k)
        a_mont = mon_mult(a_mont, a_mont, n, n_tick, k)
        # print("MONT", e, x, a_mont)
        e = e >> 1
    return mon_redc(x, n, n_tick, k)
